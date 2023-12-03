from tkinter import Tk, Label, Button, Canvas, filedialog
from PIL import Image, ImageTk, ImageOps, ImageFilter

class ImageProcessor:
    def __init__(self, root):
        self.root = root
        root.title("Xử Lý Ảnh")

        self.label = Label(root, text="Chọn ảnh để xử lý:")
        self.label.pack()

        self.canvas = Canvas(root, width=500, height=500)
        self.canvas.pack()

        self.btn_open = Button(root, text="Chọn ảnh", command=self.open_image)
        self.btn_open.pack()

        self.btn_process_negative = Button(root, text="Chuyển đổi âm bản", command=self.process_negative, state="disabled")
        self.btn_process_negative.pack()

        self.btn_process_threshold = Button(root, text="Biến đổi phân ngưỡng", command=self.process_threshold, state="disabled")
        self.btn_process_threshold.pack()

        self.btn_process_logarithmic = Button(root, text="Biến đổi logarithmic", command=self.process_logarithmic, state="disabled")
        self.btn_process_logarithmic.pack()

        self.btn_process_exponential = Button(root, text="Biến đổi hàm mũ", command=self.process_exponential, state="disabled")
        self.btn_process_exponential.pack()

        self.btn_smooth_image = Button(root, text="Làm Mịn Ảnh", command=self.process_smooth, state="disabled")
        self.btn_smooth_image.pack()
        
        self.btn_process_midpoint = Button(root, text="Midpoint Filter", command=self.process_midpoint, state="disabled")
        self.btn_process_midpoint.pack()

        self.btn_process_canny = Button(root, text="Áp dụng Canny", command=self.process_canny, state="disabled")
        self.btn_process_canny.pack()

        self.btn_process_roberts = Button(root, text="Áp dụng Roberts", command=self.process_roberts, state="disabled")
        self.btn_process_roberts.pack()


        
        self.image_path = None
        self.original_image = None
        self.processed_image = None
        self.is_negative = False

    def open_image(self):
        file_path = filedialog.askopenfilename(title="Chọn ảnh", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])

        if file_path:
            self.image_path = file_path
            self.update_image()

    def update_image(self):
        if self.image_path:
            self.original_image = Image.open(self.image_path).convert("RGB")
            self.processed_image = self.original_image.copy()
            self.processed_image.thumbnail((500, 500))
            self.photo = ImageTk.PhotoImage(self.processed_image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

            self.btn_process_negative["state"] = "normal"
            self.btn_process_threshold["state"] = "normal"
            self.btn_process_logarithmic["state"] = "normal"
            self.btn_process_exponential["state"] = "normal"
            self.btn_smooth_image["state"] = "normal"
            self.btn_process_midpoint["state"] = "normal"
            self.btn_process_canny["state"] = "normal"
            self.btn_process_roberts["state"] = "normal"

    def process_negative(self):
        if self.image_path:
            if not self.is_negative:
                self.processed_image = ImageOps.invert(self.original_image)
                self.is_negative = True
            else:
                self.processed_image = self.original_image
                self.is_negative = False

            self.processed_image.thumbnail((500, 500))
            self.photo = ImageTk.PhotoImage(self.processed_image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

    def process_threshold(self):
        if self.image_path:
            if not self.is_negative:
                gray_image = self.processed_image.convert("L")
                threshold = 128
                threshold_image = gray_image.point(lambda x: 255 if x > threshold else 0)

                self.processed_image = threshold_image
                self.is_negative = True
            else:
                self.processed_image = self.original_image
                self.is_negative = False

            self.processed_image.thumbnail((500, 500))
            self.photo = ImageTk.PhotoImage(self.processed_image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

    def process_logarithmic(self):
        if self.image_path:
            if not self.is_negative:
                gray_image = self.processed_image.convert("L")
                logarithmic_image = Image.eval(gray_image, lambda x: 20 * log(1 + x / 20))

                self.processed_image = logarithmic_image
                self.is_negative = True
            else:
                self.processed_image = self.original_image
                self.is_negative = False

            self.processed_image.thumbnail((500, 500))
            self.photo = ImageTk.PhotoImage(self.processed_image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

    def process_exponential(self):
        if self.image_path:
            if not self.is_negative:
                gray_image = self.processed_image.convert("L")
                exponential_image = Image.eval(gray_image, lambda x: exp(x / 20))

                self.processed_image = exponential_image
                self.is_negative = True
            else:
                self.processed_image = self.original_image
                self.is_negative = False

            self.processed_image.thumbnail((500, 500))
            self.photo = ImageTk.PhotoImage(self.processed_image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

    def process_smooth(self):
        if self.image_path:
            smooth_image = self.processed_image.filter(ImageFilter.BLUR)  # Bộ lọc trung bình làm mịn ảnh
            self.processed_image = smooth_image
            self.is_negative = False

            self.processed_image.thumbnail((500, 500))
            self.photo = ImageTk.PhotoImage(self.processed_image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
            
    def process_midpoint(self):
        if self.image_path:
            if not self.is_negative:
                size = 3  # Kích thước của vùng lân cận
                midpoint_image = self.original_image.filter(ImageFilter.MedianFilter(size)).filter(ImageFilter.MinFilter(size)).filter(ImageFilter.MaxFilter(size))

                self.processed_image = midpoint_image.convert("RGB")
                self.is_negative = True
            else:
                self.processed_image = self.original_image.copy()
                self.is_negative = False

            self.processed_image.thumbnail((500, 500))
            self.photo = ImageTk.PhotoImage(self.processed_image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo) 

    def process_canny(self):
            if self.image_path:
                if not self.is_negative:
                    gray_image = self.processed_image.convert("L")
                    canny_image = ImageCanny.canny(gray_image)
    
                    self.processed_image = canny_image
                    self.is_negative = True
                else:
                    self.processed_image = self.original_image
                    self.is_negative = False
    
                self.processed_image.thumbnail((500, 500))
                self.photo = ImageTk.PhotoImage(self.processed_image)
                self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

        def process_roberts(self):
            if self.image_path:
                gray_image = self.processed_image.convert("L")
                roberts_image = gray_image.filter(ImageFilter.FIND_EDGES)  # Áp dụng Roberts
        
                self.processed_image = roberts_image
                self.is_negative = False
        
                self.processed_image.thumbnail((500, 500))
                self.photo = ImageTk.PhotoImage(self.processed_image)
                self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
            
                
    

# Create an object of the ImageProcessor class
root = Tk()
image_processor = ImageProcessor(root)

# Run the application
root.mainloop()
