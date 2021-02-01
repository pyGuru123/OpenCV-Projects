import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from functools import partial

from detector import from_rgb, ColorDetector, get_color_name
from tracker import ColorTracker

cwd = os.getcwd()

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.grid()

		self.features = ['Detect Color', 'Track Color from Image', 'Track Color in Realtime']
		self.current_feature = None
		self.btn_list = []
		self.render_id = None

		self.draw_frames()
		self.draw_buttons()
#E8175D
#363636
	def draw_frames(self):
		self.topbar = tk.Frame(self, width=700, height=49, bg='#363636')
		self.imgFrame = tk.Frame(self, width=450, height=400, bg='white')
		self.rightbar = tk.Frame(self, width=250, height=200, bg='white')
		self.bottomBox = tk.Frame(self, width=250, height=200, bg='dodgerblue3') 

		self.topbar.grid(row=0, column=0, columnspan=2)
		self.imgFrame.grid(row=1, column=0, rowspan=2)
		self.rightbar.grid(row=1, column=1)
		self.bottomBox.grid(row=2, column=1)

		self.topbar.grid_propagate(False)
		self.imgFrame.grid_propagate(False)
		self.rightbar.grid_propagate(False)
		self.bottomBox.grid_propagate(False)

	def draw_buttons(self):
		cindex = 0
		for text in self.features:
			btn = tk.Button(self.topbar, text=text, width=20,
					relief=tk.RAISED, bg='dodgerblue3', fg='white')
			btn.config(command=partial(self.set_selection, btn, text))
			btn.grid(row=0, column=cindex, padx=(60,0), pady=10)
			self.btn_list.append(btn)
			cindex += 1

		self.set_selection(self.btn_list[0], self.features[0])

	def set_selection(self, widget, text):
		for w in self.imgFrame.winfo_children():
			w.destroy()

		self.canvas = tk.Canvas(self.imgFrame, width =450, height = 400, bg='#afeeee')
		self.canvas.grid(row=0, column=0)
		self.canvas.bind('<Button-1>', self.get_coord)

		for w in self.topbar.winfo_children():
			w.config(relief=tk.FLAT, bg='dodgerblue3')

		for w in self.bottomBox.winfo_children():
			w.destroy()

		for w in self.rightbar.winfo_children():
			w.destroy()

		widget.config(relief=tk.RAISED, bg='green')
		self.canvas.delete('all')
		
		if text == self.features[0]:
			self.bottomBox['bg'] = 'dodgerblue3'
			self.selection_frame(text)
			self.color_label = tk.Label(self.bottomBox, bg='dodgerblue3', fg='white', text='',
							font=('verdana 14'), width=20)
			self.color_label.grid(row=0, column=0, pady=80, padx=1)

		elif text == self.features[1]:
			self.selection_frame(text)

		elif text == self.features[2]:
			self.create_trackbar()

		self.current_feature = text

	def selection_frame(self, feature):
		if self.render_id:
			self.imgFrame.after_cancel(self.render_id)
			self.render_id = None
		for widget in self.rightbar.winfo_children():
			widget.destroy()

		if feature == self.features[0]:
			select_btn = tk.Button(self.rightbar, text='Select File', width=10,
						relief=tk.RAISED, bg='dodgerblue3', fg='white',
						command=self.select_file)
			select_btn.grid(row=0, column=0, padx=80, pady=50)

		elif feature == self.features[1]:
			select_btn = tk.Button(self.rightbar, text='Select File', width=10,
						relief=tk.RAISED, bg='dodgerblue3', fg='white',
						command=self.select_file)
			select_btn.grid(row=0, column=0, padx=80, pady=(50,10))

			self.track_btn = tk.Button(self.rightbar, text='Track Color', width=10,
						relief=tk.RAISED, bg='dodgerblue3', fg='white',
						command=self.start_tracking, state=tk.DISABLED)
			self.track_btn.grid(row=1, column=0, padx=80, pady=20)

	def select_file(self):
		self.filepath = filedialog.askopenfilename(initialdir = cwd)
		if self.filepath:
			if self.current_feature == self.features[0]:
				self.CDObj = ColorDetector(self.filepath)
				self.image = self.CDObj.display_image((450, 400))
				self.canvas.create_image(0,0,  anchor=tk.NW, image=self.image)    
				self.canvas.image = self.image 
				self.update()

			elif self.current_feature == self.features[1]:
				for w in self.bottomBox.winfo_children():
					w.destroy()
				self.TDObj = ColorTracker(self.filepath)
				self.image = self.TDObj.display_original_image((250, 200))
				self.imglabel = tk.Label(self.bottomBox, image=self.image)
				self.imglabel.grid(row=0, column=0)

				self.im = self.TDObj.display_original_image((450, 400))
				# self.canvas.create_image(0,0,  anchor=tk.NW, image=self.im)    
				# self.canvas.image = self.im 
				self.canvas.destroy()
				self.tracked_img = tk.Label(self.imgFrame, image=self.im)
				self.tracked_img.grid(row=0, column=0)
				self.update()
				self.track_btn.config(state=tk.NORMAL)

	def get_coord(self, event):
		x, y = event.x, event.y

		if self.current_feature == self.features[0]:
			color = self.CDObj.get_pixel_value((x,y))
			hex_color = from_rgb(list(color))
			self.bottomBox['bg'] = hex_color
			self.update()
			cname = get_color_name(*color)
			if sum(color) >= 600:
				fg = 'white'
			else:
				fg = 'black'
			self.color_label.config(fg=fg, text=cname)

	def start_tracking(self):
		for w in self.rightbar.winfo_children():
			w.destroy()

		self.create_trackbar()
		self.update()

	def create_trackbar(self):
		self.lh_value = tk.IntVar()
		self.ls_value = tk.IntVar()
		self.lv_value = tk.IntVar()
		self.hh_value = tk.IntVar()
		self.hs_value = tk.IntVar()
		self.hv_value = tk.IntVar()

		self.hh_value.set(255)
		self.hs_value.set(255)
		self.hv_value.set(255)

		self.slider_arr = [self.lh_value, self.ls_value, self.lv_value,
					  self.hh_value, self.hs_value, self.hv_value]

		for index, variable in enumerate(self.slider_arr):
			if  index <= 2:
				from_, to, c = 0, 255, 0
				r = (2 * index) + 1
			else:
				from_, to, c = 0, 255, 1
				r = (2 * (index - 3)) + 1

			slider = ttk.Scale(self.rightbar, from_ = from_, to = to, orient = tk.HORIZONTAL)
			slider['variable'] = variable
			slider['command'] = self.print_val
			slider.grid(row=r, column=c, padx=(12,5), pady=(2,15))

		for index, text in enumerate(['Hue (low/high)', 'Saturation (low/high)', 'Value (low/high)']):
			lbl = tk.Label(self.rightbar, text=text, width=30, anchor='w')
			lbl.grid(row=2*index, column=0, columnspan=2)

		self.render_id = self.imgFrame.after(100, self.track_color)

	def print_val(self, event=None):
		# for slider in self.slider_arr:
		# 	print(slider.get(), end=' ')
		# print()
		pass

	def track_color(self):
		if self.render_id:
			arr1 = [item.get() for item in self.slider_arr[:3]]
			arr2 = [item.get() for item in self.slider_arr[3:]]

			self.im = self.TDObj.detect_from_hsv(arr1, arr2)
			self.tracked_img['image'] = self.im
			self.update()
			# print('updated')
			self.render_id = self.imgFrame.after(100, self.track_color)
		# pass



if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('700x450+350+130')
	root.title('Color Detector & Tracker')

	app = Application(master=root)
	app.mainloop()