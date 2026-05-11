from PIL import Image
import os
import re

class ImageService:
    @staticmethod
    def get_image_info(file_path):
        try:
            with Image.open(file_path) as img:
                return {
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'mode': img.mode
                }
        except Exception:
            return None

    @staticmethod
    def detect_scale_factor(file_name):
        pattern = r'@(\d+)x'
        match = re.search(pattern, file_name)
        if match:
            return int(match.group(1))
        return 1

    @staticmethod
    def normalize_filename(file_name):
        pattern = r'@(\d+)x'
        normalized = re.sub(pattern, '', file_name)
        return normalized

    @staticmethod
    def generate_scaled_images(source_path, source_scale, output_dir):
        results = []
        try:
            with Image.open(source_path) as img:
                file_name = os.path.basename(source_path)
                normalized_name = ImageService.normalize_filename(file_name)
                name_without_ext = os.path.splitext(normalized_name)[0]
                ext = os.path.splitext(normalized_name)[1]

                scales_to_generate = []
                if source_scale == 1:
                    scales_to_generate = [(1, 1.0), (2, 2.0), (3, 3.0)]
                elif source_scale == 2:
                    scales_to_generate = [(1, 0.5), (2, 1.0), (3, 1.5)]
                elif source_scale == 3:
                    scales_to_generate = [(1, 1/3), (2, 2/3), (3, 1.0)]

                for target_scale, factor in scales_to_generate:
                    new_width = int(img.width * factor)
                    new_height = int(img.height * factor)
                    
                    if new_width <= 0 or new_height <= 0:
                        continue

                    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                    if target_scale == 1:
                        output_name = f"{name_without_ext}{ext}"
                    else:
                        output_name = f"{name_without_ext}@{target_scale}x{ext}"

                    sub_dir = os.path.join(output_dir, name_without_ext)
                    os.makedirs(sub_dir, exist_ok=True)

                    output_path = os.path.join(sub_dir, output_name)
                    resized_img.save(output_path, quality=95)
                    results.append({
                        'scale': target_scale,
                        'path': output_path,
                        'width': new_width,
                        'height': new_height
                    })

            return True, results
        except Exception as e:
            return False, str(e)

    @staticmethod
    def is_valid_image(file_path):
        valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
        return file_path.lower().endswith(valid_extensions)
