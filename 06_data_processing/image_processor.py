#!/usr/bin/env python3
"""
Image Processor Script - Basic Image Operations with PIL

This script demonstrates various image processing techniques using the Python
Imaging Library (PIL/Pillow) for common image manipulation tasks.

Author: Python Learning Series
Dependencies: Pillow, numpy
"""

from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import numpy as np
from pathlib import Path
from typing import Tuple, List, Optional, Union
import io
import sys


class ImageProcessor:
    """
    A comprehensive image processing class that provides methods for
    loading, manipulating, and saving images using PIL/Pillow.
    """
    
    def __init__(self, image_path: Optional[str] = None):
        """
        Initialize the ImageProcessor.
        
        Args:
            image_path: Optional path to load an image
        """
        self.original_image = None
        self.current_image = None
        self.image_path = image_path
        
        if image_path:
            self.load_image(image_path)
    
    def load_image(self, image_path: str) -> bool:
        """
        Load an image from file.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            bool: True if image loaded successfully
        """
        try:
            if not Path(image_path).exists():
                print(f"Error: Image file '{image_path}' not found.")
                return False
            
            self.original_image = Image.open(image_path)
            self.current_image = self.original_image.copy()
            self.image_path = image_path
            
            print(f"Successfully loaded image: {image_path}")
            print(f"Image format: {self.original_image.format}")
            print(f"Image size: {self.original_image.size}")
            print(f"Image mode: {self.original_image.mode}")
            
            return True
            
        except Exception as e:
            print(f"Error loading image: {e}")
            return False
    
    def create_sample_image(self, width: int = 400, height: int = 300,
                           color: str = 'RGB') -> Image.Image:
        """
        Create a sample image for demonstration purposes.
        
        Args:
            width: Image width in pixels
            height: Image height in pixels
            color: Color mode ('RGB', 'RGBA', 'L')
            
        Returns:
            PIL.Image: Created sample image
        """
        try:
            # Create a gradient background
            if color == 'RGB':
                img = Image.new('RGB', (width, height), color='white')
                
                # Create gradient effect
                for y in range(height):
                    for x in range(width):
                        r = int(255 * x / width)
                        g = int(255 * y / height)
                        b = int(255 * (x + y) / (width + height))
                        img.putpixel((x, y), (r, g, b))
                        
            elif color == 'L':
                img = Image.new('L', (width, height), color=128)
                
            else:
                img = Image.new(color, (width, height), color='white')
            
            # Add some shapes for visual interest
            draw = ImageDraw.Draw(img)
            
            # Draw circles
            for i in range(5):
                x = width // 6 * (i + 1)
                y = height // 2
                radius = 20 + i * 10
                
                if color == 'RGB':
                    circle_color = (255 - i * 40, i * 40, 128)
                else:
                    circle_color = 200 - i * 20
                
                draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                           outline=circle_color, width=3)
            
            # Add text
            try:
                font = ImageFont.load_default()
                draw.text((10, 10), "Sample Image", fill=(0, 0, 0) if color == 'RGB' else 0,
                         font=font)
            except:
                draw.text((10, 10), "Sample Image", fill=(0, 0, 0) if color == 'RGB' else 0)
            
            self.current_image = img
            print(f"Created sample {color} image: {width}x{height}")
            
            return img
            
        except Exception as e:
            print(f"Error creating sample image: {e}")
            return None
    
    def get_image_info(self) -> dict:
        """
        Get detailed information about the current image.
        
        Returns:
            dict: Dictionary containing image information
        """
        if self.current_image is None:
            print("No image loaded.")
            return {}
        
        try:
            info = {
                'size': self.current_image.size,
                'width': self.current_image.width,
                'height': self.current_image.height,
                'mode': self.current_image.mode,
                'format': getattr(self.current_image, 'format', 'Unknown'),
                'has_transparency': self.current_image.mode in ('RGBA', 'LA', 'P'),
                'bands': self.current_image.getbands(),
                'extrema': self.current_image.getextrema() if self.current_image.mode in ('L', 'RGB') else None
            }
            
            # Calculate file size estimate
            img_array = np.array(self.current_image)
            info['array_shape'] = img_array.shape
            info['memory_size_kb'] = img_array.nbytes / 1024
            
            return info
            
        except Exception as e:
            print(f"Error getting image info: {e}")
            return {}
    
    def resize_image(self, width: int, height: int, 
                    maintain_aspect: bool = True) -> bool:
        """
        Resize the image to specified dimensions.
        
        Args:
            width: Target width
            height: Target height
            maintain_aspect: Whether to maintain aspect ratio
            
        Returns:
            bool: True if resize successful
        """
        if self.current_image is None:
            print("No image loaded.")
            return False
        
        try:
            if maintain_aspect:
                # Calculate aspect ratio preserving dimensions
                original_width, original_height = self.current_image.size
                aspect_ratio = original_width / original_height
                
                if width / height > aspect_ratio:
                    # Height is the limiting factor
                    width = int(height * aspect_ratio)
                else:
                    # Width is the limiting factor
                    height = int(width / aspect_ratio)
            
            # Use high-quality resampling
            self.current_image = self.current_image.resize(
                (width, height), Image.Resampling.LANCZOS
            )
            
            print(f"Image resized to: {width}x{height}")
            return True
            
        except Exception as e:
            print(f"Error resizing image: {e}")
            return False
    
    def rotate_image(self, angle: float, expand: bool = True) -> bool:
        """
        Rotate the image by specified angle.
        
        Args:
            angle: Rotation angle in degrees (positive = counterclockwise)
            expand: Whether to expand image to fit rotated content
            
        Returns:
            bool: True if rotation successful
        """
        if self.current_image is None:
            print("No image loaded.")
            return False
        
        try:
            self.current_image = self.current_image.rotate(
                angle, expand=expand, fillcolor='white'
            )
            
            print(f"Image rotated by {angle} degrees")
            return True
            
        except Exception as e:
            print(f"Error rotating image: {e}")
            return False
    
    def flip_image(self, direction: str = 'horizontal') -> bool:
        """
        Flip the image horizontally or vertically.
        
        Args:
            direction: 'horizontal' or 'vertical'
            
        Returns:
            bool: True if flip successful
        """
        if self.current_image is None:
            print("No image loaded.")
            return False
        
        try:
            if direction.lower() == 'horizontal':
                self.current_image = self.current_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                print("Image flipped horizontally")
            elif direction.lower() == 'vertical':
                self.current_image = self.current_image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                print("Image flipped vertically")
            else:
                print("Direction must be 'horizontal' or 'vertical'")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error flipping image: {e}")
            return False
    
    def crop_image(self, left: int, top: int, right: int, bottom: int) -> bool:
        """
        Crop the image to specified coordinates.
        
        Args:
            left: Left coordinate
            top: Top coordinate
            right: Right coordinate
            bottom: Bottom coordinate
            
        Returns:
            bool: True if crop successful
        """
        if self.current_image is None:
            print("No image loaded.")
            return False
        
        try:
            # Validate coordinates
            width, height = self.current_image.size
            
            if left < 0 or top < 0 or right > width or bottom > height:
                print("Crop coordinates are outside image boundaries")
                return False
            
            if left >= right or top >= bottom:
                print("Invalid crop coordinates")
                return False
            
            self.current_image = self.current_image.crop((left, top, right, bottom))
            
            print(f"Image cropped to: {right-left}x{bottom-top}")
            return True
            
        except Exception as e:
            print(f"Error cropping image: {e}")
            return False
    
    def apply_filter(self, filter_type: str) -> bool:
        """
        Apply various filters to the image.
        
        Args:
            filter_type: Type of filter to apply
            
        Returns:
            bool: True if filter applied successfully
        """
        if self.current_image is None:
            print("No image loaded.")
            return False
        
        try:
            filter_map = {
                'blur': ImageFilter.BLUR,
                'detail': ImageFilter.DETAIL,
                'edge_enhance': ImageFilter.EDGE_ENHANCE,
                'edge_enhance_more': ImageFilter.EDGE_ENHANCE_MORE,
                'emboss': ImageFilter.EMBOSS,
                'find_edges': ImageFilter.FIND_EDGES,
                'sharpen': ImageFilter.SHARPEN,
                'smooth': ImageFilter.SMOOTH,
                'smooth_more': ImageFilter.SMOOTH_MORE,
                'contour': ImageFilter.CONTOUR
            }
            
            if filter_type.lower() not in filter_map:
                available_filters = ', '.join(filter_map.keys())
                print(f"Unknown filter. Available filters: {available_filters}")
                return False
            
            self.current_image = self.current_image.filter(filter_map[filter_type.lower()])
            
            print(f"Applied {filter_type} filter")
            return True
            
        except Exception as e:
            print(f"Error applying filter: {e}")
            return False
    
    def adjust_brightness(self, factor: float) -> bool:
        """
        Adjust image brightness.
        
        Args:
            factor: Brightness factor (1.0 = no change, >1.0 = brighter, <1.0 = darker)
            
        Returns:
            bool: True if adjustment successful
        """
        if self.current_image is None:
            print("No image loaded.")
            return False
        
        try:
            enhancer = ImageEnhance.Brightness(self.current_image)
            self.current_image = enhancer.enhance(factor)
            
            print(f"Brightness adjusted by factor {factor}")
            return True
            
        except Exception as e:
            print(f"Error adjusting brightness: {e}")
            return False
    
    def adjust_contrast(self, factor: float) -> bool:
        """
        Adjust image contrast.
        
        Args:
            factor: Contrast factor (1.0 = no change, >1.0 = more contrast, <1.0 = less contrast)
            
        Returns:
            bool: True if adjustment successful
        """
        if self.current_image is None:
            print("No image loaded.")
            return False
        
        try:
            enhancer = ImageEnhance.Contrast(self.current_image)
            self.current_image = enhancer.enhance(factor)
            
            print(f"Contrast adjusted by factor {factor}")
            return True
            
        except Exception as e:
            print(f"Error adjusting contrast: {e}")
            return False
    
    def adjust_color(self, factor: float) -> bool:
        """
        Adjust image color saturation.
        
        Args:
            factor: Color factor (1.0 = no change, >1.0 = more saturated, 0.0 = grayscale)
            
        Returns:
            bool: True if adjustment successful
        """
        if self.current_image is None:
            print("No image loaded.")
            return False
        
        try:
            if self.current_image.mode not in ('RGB', 'RGBA'):
                print("Color adjustment requires RGB or RGBA image")
                return False
            
            enhancer = ImageEnhance.Color(self.current_image)
            self.current_image = enhancer.enhance(factor)
            
            print(f"Color saturation adjusted by factor {factor}")
            return True
            
        except Exception as e:
            print(f"Error adjusting color: {e}")
            return False
    
    def convert_to_grayscale(self) -> bool:
        """
        Convert image to grayscale.
        
        Returns:
            bool: True if conversion successful
        """
        if self.current_image is None:
            print("No image loaded.")
            return False
        
        try:
            self.current_image = self.current_image.convert('L')
            
            print("Image converted to grayscale")
            return True
            
        except Exception as e:
            print(f"Error converting to grayscale: {e}")
            return False
    
    def add_text_watermark(self, text: str, position: str = 'bottom-right',
                          font_size: int = 36, opacity: int = 128) -> bool:
        """
        Add a text watermark to the image.
        
        Args:
            text: Watermark text
            position: Position ('top-left', 'top-right', 'bottom-left', 'bottom-right', 'center')
            font_size: Font size
            opacity: Text opacity (0-255)
            
        Returns:
            bool: True if watermark added successfully
        """
        if self.current_image is None:
            print("No image loaded.")
            return False
        
        try:
            # Create a transparent overlay
            overlay = Image.new('RGBA', self.current_image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Try to load a font
            try:
                font = ImageFont.load_default()
            except:
                font = None
            
            # Get text dimensions
            if font:
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            else:
                # Estimate text size
                text_width = len(text) * font_size // 2
                text_height = font_size
            
            # Calculate position
            img_width, img_height = self.current_image.size
            
            position_map = {
                'top-left': (10, 10),
                'top-right': (img_width - text_width - 10, 10),
                'bottom-left': (10, img_height - text_height - 10),
                'bottom-right': (img_width - text_width - 10, img_height - text_height - 10),
                'center': (img_width // 2 - text_width // 2, img_height // 2 - text_height // 2)
            }
            
            if position not in position_map:
                print(f"Invalid position. Available positions: {', '.join(position_map.keys())}")
                return False
            
            x, y = position_map[position]
            
            # Draw text on overlay
            text_color = (255, 255, 255, opacity)  # White with specified opacity
            draw.text((x, y), text, fill=text_color, font=font)
            
            # Convert current image to RGBA if needed
            if self.current_image.mode != 'RGBA':
                rgba_image = self.current_image.convert('RGBA')
            else:
                rgba_image = self.current_image
            
            # Composite the overlay onto the image
            self.current_image = Image.alpha_composite(rgba_image, overlay)
            
            print(f"Added watermark '{text}' at {position}")
            return True
            
        except Exception as e:
            print(f"Error adding watermark: {e}")
            return False
    
    def create_thumbnail(self, max_size: Tuple[int, int] = (128, 128)) -> Optional[Image.Image]:
        """
        Create a thumbnail of the current image.
        
        Args:
            max_size: Maximum size as (width, height) tuple
            
        Returns:
            PIL.Image: Thumbnail image
        """
        if self.current_image is None:
            print("No image loaded.")
            return None
        
        try:
            thumbnail = self.current_image.copy()
            thumbnail.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            print(f"Created thumbnail: {thumbnail.size}")
            return thumbnail
            
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return None
    
    def save_image(self, output_path: str, quality: int = 95,
                  optimize: bool = True) -> bool:
        """
        Save the current image to file.
        
        Args:
            output_path: Path to save the image
            quality: JPEG quality (1-100)
            optimize: Whether to optimize the image
            
        Returns:
            bool: True if save successful
        """
        if self.current_image is None:
            print("No image to save.")
            return False
        
        try:
            # Create directory if it doesn't exist
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Determine save parameters based on file format
            save_kwargs = {'optimize': optimize}
            
            file_ext = Path(output_path).suffix.lower()
            if file_ext in ['.jpg', '.jpeg']:
                save_kwargs['quality'] = quality
                # Convert RGBA to RGB for JPEG
                if self.current_image.mode == 'RGBA':
                    rgb_image = Image.new('RGB', self.current_image.size, (255, 255, 255))
                    rgb_image.paste(self.current_image, mask=self.current_image.split()[-1])
                    rgb_image.save(output_path, **save_kwargs)
                else:
                    self.current_image.save(output_path, **save_kwargs)
            else:
                self.current_image.save(output_path, **save_kwargs)
            
            print(f"Image saved to: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error saving image: {e}")
            return False
    
    def reset_to_original(self) -> bool:
        """
        Reset the current image to the original.
        
        Returns:
            bool: True if reset successful
        """
        if self.original_image is None:
            print("No original image available.")
            return False
        
        try:
            self.current_image = self.original_image.copy()
            print("Image reset to original")
            return True
            
        except Exception as e:
            print(f"Error resetting image: {e}")
            return False
    
    def get_image_statistics(self) -> dict:
        """
        Get statistical information about the image.
        
        Returns:
            dict: Dictionary containing image statistics
        """
        if self.current_image is None:
            print("No image loaded.")
            return {}
        
        try:
            # Convert to numpy array for analysis
            img_array = np.array(self.current_image)
            
            stats = {
                'shape': img_array.shape,
                'min_value': int(np.min(img_array)),
                'max_value': int(np.max(img_array)),
                'mean_value': float(np.mean(img_array)),
                'std_value': float(np.std(img_array)),
                'unique_colors': len(np.unique(img_array.reshape(-1, img_array.shape[-1]), axis=0)) if len(img_array.shape) == 3 else len(np.unique(img_array))
            }
            
            return stats
            
        except Exception as e:
            print(f"Error calculating statistics: {e}")
            return {}


def main():
    """
    Demonstrate the ImageProcessor class with various operations.
    
    Usage Examples:
    1. Process existing image:
       python image_processor.py path/to/image.jpg
       
    2. Create and process sample image:
       python image_processor.py
       
    3. Batch process multiple operations:
       processor = ImageProcessor('image.jpg')
       processor.resize_image(800, 600)
       processor.apply_filter('blur')
       processor.save_image('processed_image.jpg')
    """
    print("Image Processor - Demonstration")
    print("=" * 40)
    
    try:
        # Check if image path provided as command line argument
        if len(sys.argv) > 1:
            image_path = sys.argv[1]
            print(f"Loading image from: {image_path}")
            processor = ImageProcessor(image_path)
        else:
            print("No image path provided. Creating sample image...")
            processor = ImageProcessor()
            processor.create_sample_image(600, 400)
        
        if processor.current_image is None:
            print("Failed to load or create image. Exiting.")
            return
        
        # Create output directory
        output_dir = Path("processed_images")
        output_dir.mkdir(exist_ok=True)
        
        print(f"\nProcessed images will be saved to: {output_dir.absolute()}")
        
        # Display image information
        print("\n1. IMAGE INFORMATION")
        print("-" * 20)
        info = processor.get_image_info()
        for key, value in info.items():
            print(f"{key}: {value}")
        
        # Get image statistics
        print("\n2. IMAGE STATISTICS")
        print("-" * 20)
        stats = processor.get_image_statistics()
        for key, value in stats.items():
            print(f"{key}: {value}")
        
        # Demonstrate various operations
        print("\n3. APPLYING TRANSFORMATIONS")
        print("-" * 30)
        
        # Save original
        processor.save_image(str(output_dir / "01_original.png"))
        
        # Resize
        processor.resize_image(400, 300, maintain_aspect=True)
        processor.save_image(str(output_dir / "02_resized.png"))
        
        # Reset and apply filter
        processor.reset_to_original()
        processor.apply_filter('blur')
        processor.save_image(str(output_dir / "03_blur_filter.png"))
        
        # Reset and adjust brightness
        processor.reset_to_original()
        processor.adjust_brightness(1.5)
        processor.save_image(str(output_dir / "04_brightness.png"))
        
        # Reset and adjust contrast
        processor.reset_to_original()
        processor.adjust_contrast(1.5)
        processor.save_image(str(output_dir / "05_contrast.png"))
        
        # Reset and convert to grayscale
        processor.reset_to_original()
        processor.convert_to_grayscale()
        processor.save_image(str(output_dir / "06_grayscale.png"))
        
        # Reset and add watermark
        processor.reset_to_original()
        processor.add_text_watermark("SAMPLE", position='bottom-right')
        processor.save_image(str(output_dir / "07_watermark.png"))
        
        # Reset and rotate
        processor.reset_to_original()
        processor.rotate_image(45)
        processor.save_image(str(output_dir / "08_rotated.png"))
        
        # Reset and crop (center portion)
        processor.reset_to_original()
        width, height = processor.current_image.size
        crop_margin = min(width, height) // 4
        processor.crop_image(crop_margin, crop_margin, 
                           width - crop_margin, height - crop_margin)
        processor.save_image(str(output_dir / "09_cropped.png"))
        
        # Create thumbnail
        processor.reset_to_original()
        thumbnail = processor.create_thumbnail((150, 150))
        if thumbnail:
            thumbnail.save(str(output_dir / "10_thumbnail.png"))
        
        print(f"\nProcessing complete!")
        print(f"Check the '{output_dir}' directory for all processed images.")
        
        # Display final statistics
        print(f"\nFinal image size: {processor.current_image.size}")
        print(f"Final image mode: {processor.current_image.mode}")
        
    except Exception as e:
        print(f"Error in main execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()