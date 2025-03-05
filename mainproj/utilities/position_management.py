from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.apps import apps
from django.db import transaction
from django.db.models import F, Max,Min
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PositionManagementViewSet(viewsets.ViewSet):

    # Mapping of frontend identifiers to actual model names
    MODEL_MAP = {
        # 'meet-team':('components','MeetTeam'),
        'duration':('duration','Duration'),
        'event-gallery':('event','EventGallery'),
        'event':('event','Event'),
        # 'gallery': ('gallery', 'Gallery'),
        # 'gallery-group': ('gallery', 'GalleryGroup'),
        # 'quotation': ('quotationmanagement', 'Quotation'),
        # 'booking': ('bookingmanagement', 'BookingService'),
        # 'service-category': ('service_category_management', 'Category'),
        # 'service': ('servicemanagement', 'Service'),
        # 'blog': ('blog', 'Blog'),
        # 'customer-inquiry': ('customerinquiries', 'CustomerInquiries'),
        # 'branch': ('branchdetails', 'Branch'),
        # 'review': ('review', 'Review'),
    }

    BREATH_HOLD = 10  # Maximum distance for small moves
    def _get_model(self, model_key):
        """
        Retrieve model class based on model key.
        """
        model_info = self.MODEL_MAP.get(model_key)
        if model_info:
            app_label, model_name = model_info
            try:
                return apps.get_model(app_label, model_name)
            except LookupError:
                return None
        return None
    
    @swagger_auto_schema(
    method='get',
    operation_summary="Move an item to a new position",
    operation_description=(
        "Moves an item from `target` position to `goal` position within the specified `model`.\n\n"
        "**Keys:**\n"
        "- `duration`\n"
        "- `event-gallery`\n"
        "- `event`\n"
    ),
    manual_parameters=[
        openapi.Parameter('model', openapi.IN_QUERY, description="Name of the model", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('target', openapi.IN_QUERY, description="Current position of the item", type=openapi.TYPE_INTEGER, required=True),
        openapi.Parameter('goal', openapi.IN_QUERY, description="Target position for the item", type=openapi.TYPE_INTEGER, required=True),
    ],
    responses={
        200: openapi.Response("Item moved successfully"),
        400: openapi.Response("Invalid request"),
        404: openapi.Response("Target object not found"),
    }
)


    

    @action(detail=False, methods=['get'], url_path='drag-item')
    def draggable(self, request, *args, **kwargs):
        model_name = request.GET.get('model')
        target_position = request.GET.get('target')
        goal_position = request.GET.get('goal')
        breath_hold = self.BREATH_HOLD

        if not model_name or target_position is None or goal_position is None:
            return Response({"error": "Model name, target, or goal position not provided"}, status=400)

        # Load the model
        Model = self._get_model(model_name)
        if Model is None:
            return Response({"error": f"Model '{model_name}' not found"}, status=400)

        # Convert positions to integers
        try:
            target_position = int(target_position)
            goal_position = int(goal_position)
        except ValueError:
            return Response({"error": "Invalid target or goal position"}, status=400)

        # Fetch the target object
        try:
            target_obj = Model.objects.get(position=target_position)
        except Model.DoesNotExist:
            return Response({"error": "Target object not found"}, status=400)

        # Validate goal position range
        current_positions = Model.objects.values_list('position', flat=True)
        if goal_position not in current_positions and goal_position != 0:  # Allow moving to position 0
            return Response({"error": "Goal position is out of bounds"}, status=400)

        # Calculate move distance and choose strategy
        distance = abs(goal_position - target_position)

        if distance <= breath_hold:
            return self._small_move_strategy(Model, target_obj, target_position, goal_position)
        elif target_position == 0:  # Already at the front
            return self._back_move_strategy(Model, target_obj, target_position, goal_position)
        elif target_position == max(current_positions):  # Already at the end
            return self._front_move_strategy(Model, target_obj, target_position, goal_position)
        else:
            return self._big_jump_strategy(Model, target_obj, target_position, goal_position)

    def _small_move_strategy(self, Model, target_obj, target_position, goal_position):
        try:
            with transaction.atomic():
                if target_position < goal_position:
                    # Moving down
                    Model.objects.filter(position__gt=target_position, position__lte=goal_position).update(position=F('position') - 1)
                else:
                    # Moving up
                    Model.objects.filter(position__lt=target_position, position__gte=goal_position).update(position=F('position') + 1)

                target_obj.position = goal_position
                target_obj.save()

            return Response({"status": "success", "message": "Position updated successfully."})
        except Exception as e:
            return Response({"error": f"Failed to update position: {str(e)}"}, status=400)

    def _front_move_strategy(self, Model, target_obj, target_position, goal_position):
        try:
            with transaction.atomic():
                # Adjust positions of all items above the goal position
                Model.objects.filter(position__lt=target_position).update(position=F('position') + 1)
                
                # Instead of setting to 0, assign the next available position
                # Find the minimum position in the model
                min_position = Model.objects.aggregate(min_pos=Min('position'))['min_pos'] or 0
                
                # Set the target object's position to one less than the current minimum
                target_obj.position = min_position - 1 if min_position > 0 else 0
                target_obj.save()

            return Response({"status": "success", "message": "Position updated successfully."})
        except Exception as e:
            return Response({"error": f"Failed to update position: {str(e)}"}, status=400)


    def _back_move_strategy(self, Model, target_obj, target_position, goal_position):
        try:
            with transaction.atomic():
                # Move the target object to the end (max_position + 1)
                max_position = Model.objects.aggregate(max_pos=Max('position'))['max_pos'] or 0
                target_obj.position = max_position + 1
                target_obj.save()

            return Response({"status": "success", "message": "Position updated successfully."})
        except Exception as e:
            return Response({"error": f"Failed to update position: {str(e)}"}, status=400)

    def _big_jump_strategy(self, Model, target_obj, target_position, goal_position):
        try:
            with transaction.atomic():
                if goal_position > target_position:
                    # Moving down (to a higher position)
                    Model.objects.filter(position__gt=target_position, position__lt=goal_position).update(position=F('position') - 1)
                else:
                    # Moving up (to a lower position)
                    Model.objects.filter(position__lt=target_position, position__gte=goal_position).update(position=F('position') + 1)

                # Set the target object's position to the goal position with a decimal
                target_obj.position = goal_position + 0.5  # Use a decimal position
                target_obj.save()

            return Response({
                "status": "success",
                "message": "Position updated successfully.",
                "new_position": target_obj.position  # Return the decimal position
            })
        except Exception as e:
            return Response({"error": f"Failed to update position: {str(e)}"}, status=400)
