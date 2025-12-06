from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import cloudinary.uploader
import uuid
from .. import models
from .. import serializers
from PIL import Image
import io
class ImageManageAPIView(APIView):

    def get(self, request, pk=None, product_id=None):
        # Get image_type from query parameters and validate
        image_type = request.query_params.get('image_type')
        if image_type and not isinstance(image_type, str):
            return Response({"error": "Invalid image_type provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check for pk and fetch single image
            if pk:
                image = models.Image.objects.get(id=pk)
                serializer = serializers.ImageSerializer(image)
                return Response(serializer.data, status=status.HTTP_200_OK)

            # Fetch images based on product_id and/or image_type
            images = models.Image.objects.all()  # Default to all images

            if product_id:
                images = images.filter(product_id=product_id)

            if image_type:
                images = images.filter(image_type=image_type)

            # If no images found, return empty list with 200 status
            if not images.exists():
                return Response([], status=status.HTTP_200_OK)

            # Serialize and return images
            serializer = serializers.ImageSerializer(images, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except models.Image.DoesNotExist:
            return Response({"error": "Image not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "An error occurred while fetching images."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def post(self, request):
        print("POST request received.")
        product_id = request.data.get('product')
        image_type = request.data.get('image_type', 'product')
        print(f"Product ID from request: {product_id}")
        print(f"Image Type from request: {image_type}")

        image_file = request.FILES.get('image')
        if not image_file:
            print("Error: No image file provided.")
            return Response({"error": "No image file provided."}, status=status.HTTP_400_BAD_REQUEST)

        image_uuid = uuid.uuid4()
        print(f"Generated UUID for image: {image_uuid}")

        # Upload image to Cloudinary and get the URL
        image_url = self.upload_image_to_cloudinary(product_id, image_uuid, image_file)
        if not image_url:
            return Response({"error": "Failed to upload image to Cloudinary."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print(f"Generated Cloudinary URL: {image_url}")

        # Save the image instance to the database
        image_instance = models.Image(product_id=product_id, image_url=image_url, image_type=image_type)
        image_instance.save()
        print("Image instance saved to database.")

        # Serialize and return the response
        serializer = serializers.ImageSerializer(image_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        print("DELETE request received.")
        image_id = request.data.get('id')
        if not image_id:
            return Response({"error": "Image ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the image instance from the database
            image = models.Image.objects.get(id=image_id)

            # Delete image from Cloudinary (if needed, but Cloudinary handles deletion via API if required)
            # For now, just delete from database as Cloudinary URLs can be managed separately

            # Delete image from database
            image.delete()
            print("Image deleted from database.")

            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Image.DoesNotExist:
            print("Image not found in the database.")
            return Response({"error": "Image not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error during deletion: {str(e)}")
            return Response({"error": "An error occurred while deleting the image."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def upload_image_to_cloudinary(self, product_id, image_uuid, image_file):
        # Get product name for folder structure
        product_name = self.get_product_name(product_id)
        sanitized_product_name = self.format_product_name(product_name)

        # Define the public_id using the sanitized product name and image UUID
        public_id = f"{sanitized_product_name}/{image_uuid}"

        # Upload the image to Cloudinary
        try:
            upload_result = cloudinary.uploader.upload(
                image_file,
                public_id=public_id,
                folder="blackwilbur/images",  # Optional: organize in a folder
                overwrite=True,
                resource_type="image"
            )
            # Return the secure URL of the uploaded image
            return upload_result['secure_url']
        except Exception as e:
            print(f"Error uploading image to Cloudinary: {e}")
            return None

    def get_product_name(self, product_id):
        try:
            product = models.Product.objects.get(id=product_id)
            return product.name
        except models.Product.DoesNotExist:
            return "Unknown Product"

    def format_product_name(self, product_name):
        formatted_name = product_name.strip().lower().replace(" ", "-")
        return formatted_name.rstrip('-')

    def put(self, request):
        """
        Update an existing image in Cloudinary and database.

        Expected request data:
        - id: ID of the existing image to update
        - product: (optional) new product ID
        - image: new image file
        - image_type: (optional) new image type
        """
        print("PUT request received for image update.")

        # Validate required parameters
        image_id = request.data.get('id')
        if not image_id:
            return Response({"error": "Image ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the existing image instance
            existing_image = models.Image.objects.get(id=image_id)

            # Check if a new image file is provided
            new_image_file = request.FILES.get('image')
            if not new_image_file:
                return Response({"error": "New image file is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Generate a new UUID for the image
            new_image_uuid = uuid.uuid4()

            # Determine product ID (use existing or new)
            product_id = request.data.get('product', existing_image.product_id)

            # Upload new image to Cloudinary and get the URL
            new_image_url = self.upload_image_to_cloudinary(product_id, new_image_uuid, new_image_file)
            if not new_image_url:
                return Response({"error": "Failed to upload new image to Cloudinary."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Update image instance in database
            existing_image.product_id = product_id
            existing_image.image_url = new_image_url
            existing_image.image_type = request.data.get('image_type', existing_image.image_type)
            existing_image.save()

            print("Image updated successfully.")

            # Serialize and return the updated image
            serializer = serializers.ImageSerializer(existing_image)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except models.Image.DoesNotExist:
            return Response({"error": "Image not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error during image update: {str(e)}")
            return Response({"error": "An error occurred while updating the image."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
