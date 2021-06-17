import tkinter as tk
from tkinter import messagebox as msg
from PIL import Image, ImageTk

class AppPage(tk.Frame):

	def __init__(self, parent, App):
		self.app = App
		self.settings = App.settings
		self.current_product = self.settings.products[0]
		self.last_current_product_index = 0
		self.update_mode = False
		self.products_index = []

		super().__init__(parent) #parent = window.container
		self.grid(row=0, column=0, sticky="nsew")

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.create_left_frame()
		self.create_right_frame()
		self.config_left_and_right_frame()		

	def create_left_frame(self):
		self.left_frame = tk.Frame(self, bg="pink")
		self.left_frame.grid(row=0, column=0, sticky="nsew")

		self.create_left_header()
		self.create_left_content()

	def create_right_frame(self):
		self.right_frame = tk.Frame(self, bg="white", width=2*self.settings.width//3)
		self.right_frame.grid(row=0, column=1, sticky="nsew")

		self.create_right_header()
		self.create_right_content()
		self.create_right_footer()

	def config_left_and_right_frame(self):
		self.grid_columnconfigure(0, weight=1) # 1/3
		self.grid_columnconfigure(1, weight=2) # 2/3
		self.grid_rowconfigure(0, weight=1)

	def create_left_header(self):
		frame_w = self.settings.width//3
		frame_h = self.settings.height//5
		self.left_header = tk.Frame(self.left_frame, width=frame_w, height=frame_h)
		self.left_header.pack()

		image = Image.open(self.settings.logo)
		i_w, i_h = image.size
		ratio = i_w/frame_w
		new_size = (int(i_w/ratio), int(i_h/ratio)) # (x,y)
		image = image.resize(new_size)
		self.logo = ImageTk.PhotoImage(image)

		self.label_logo = tk.Label(self.left_header, image=self.logo)
		self.label_logo.pack()

		self.search_box_frame = tk.Frame(self.left_frame, bg="white", width=frame_w, height=frame_h//4)
		self.search_box_frame.pack(fill="x")

		self.entry_search_var = tk.StringVar()
		self.entry_search = tk.Entry(self.search_box_frame, bg="white", fg="black", font=("Arial", 12), textvariable=self.entry_search_var)
		self.entry_search.grid(row=0, column=0)

		self.button_search = tk.Button(self.search_box_frame, bg="white", fg="black", text="Find", font=("Arial", 12), command=self.clicked_search_btn)
		self.button_search.grid(row=0, column=1)

		self.search_box_frame.grid_columnconfigure(0, weight=3)
		self.search_box_frame.grid_columnconfigure(1, weight=1)

	def show_list_products_in_listbox(self):
		products = self.settings.products
		for index in self.products_index:
			product = products[index]
			for kode, info in product.items():
				nama_produk = f"{info['produk']}"
				self.products_list_box.insert("end", nama_produk)

	def show_all_product_in_listbox(self):
		self.products_list_box.delete(0, 'end')
		products = self.settings.products
		self.products_index = []
		counter = 0
		for product in products:
			self.products_index.append(counter)
			counter += 1
		self.show_list_products_in_listbox()

	def create_left_content(self):
		frame_w = self.settings.width//3
		frame_h = 4*self.settings.height//5
		self.left_content = tk.Frame(self.left_frame, width=frame_w, height=frame_h, bg="white")
		self.left_content.pack(fill="x")

		self.products_list_box = tk.Listbox(self.left_content, bg="white", fg="black", font=("Arial", 12), height=frame_h)
		self.products_list_box.pack(side="left", fill="both", expand=True)

		self.products_scroll = tk.Scrollbar(self.left_content)
		self.products_scroll.pack(side="right", fill="y")

		self.show_all_product_in_listbox()

		self.products_list_box.configure(yscrollcommand=self.products_scroll.set) # set di Scroll
		self.products_scroll.configure(command=self.products_list_box.yview) # yview di Listbox

		self.products_list_box.bind("<<ListboxSelect>>", self.clicked_item_inListBox)


	def clicked_item_inListBox(self, event):
		if not self.update_mode:
			selection = event.widget.curselection()
			try :
				clicked_item_index = selection[0]
			except IndexError:
				clicked_item_index = self.last_current_product_index
			index = self.products_index[clicked_item_index]
			self.last_current_product_index = index
			self.current_product = self.settings.products[index]
			print(clicked_item_index,"=>",index)
			for kodeProduct, info in self.current_product.items():
				kode = kodeProduct
				nama_produk = info['produk']
				lokasi = info['lokasi']
				harga = info['harga']
				jumlah = info['jumlah']

			self.nama_produk_label.configure(text=nama_produk)
			self.table_info[0][1].configure(text=kode)
			self.table_info[1][1].configure(text=harga)
			self.table_info[2][1].configure(text=jumlah)
			self.table_info[3][1].configure(text=lokasi)


	def create_right_header(self):
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.right_header = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="bisque")
		self.right_header.pack()
		self.create_detail_right_header()

	def create_detail_right_header(self):
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_header = tk.Frame(self.right_header, width=frame_w, height=frame_h, bg="green")
		self.detail_header.grid(row=0, column=0, sticky="nsew")

		data_dictionary = list(self.current_product.values())[0]
		nama_produk = f"{data_dictionary['produk']}"
		self.virt_img = tk.PhotoImage(width=1, height=1)
		self.nama_produk_label = tk.Label(self.detail_header, text=nama_produk, font=("Arial", 30), width=frame_w, height=frame_h, image=self.virt_img, compound='c', bg="white")
		self.nama_produk_label.pack()

		self.right_header.grid_rowconfigure(0, weight=1)
		self.right_header.grid_columnconfigure(0, weight=1)


	def create_right_content(self):
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4

		self.right_content = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_content.pack(expand=True, pady=90)
		self.create_detail_right_content()

	def create_detail_right_content(self):
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4

		self.detail_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_content.grid(row=0, column=0, sticky="nsew")

		for kodeProduct, info in self.current_product.items():
			info = [
				['Kode Produk :', kodeProduct],
				['Harga :', info['harga']],
				['Jumlah :', info['jumlah']],
				['Lokasi :', info['lokasi']]
			]
		self.table_info = []
		rows, columns = len(info), len(info[0]) # 3, 2
		for row in range(rows):
			aRow = []
			for column in range(columns):
				label = tk.Label(self.detail_content, text=info[row][column], font=("Arial", 12), bg="white")
				aRow.append(label)
				if column == 0:
					sticky = "e"
				else:
					sticky = "w"
				label.grid(row=row, column=column, sticky=sticky)
			self.table_info.append(aRow)


		self.right_content.grid_rowconfigure(0, weight=1)
		self.right_content.grid_columnconfigure(0, weight=1)


	def create_right_footer(self):
		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.right_footer = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_footer.pack(expand=True)

		self.create_detail_right_footer()


	def create_detail_right_footer(self):
		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.detail_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Update', 'Delete', 'Add New']
		commands = [self.clicked_update_btn, self.clicked_delete_btn, self.clicked_add_new_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_footer, text=feature, bg="white", fg="black", bd=0, font=("Arial", 12, "bold"), command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20)
			self.buttons_features.append(button)

		self.right_footer.grid_rowconfigure(0, weight=1)
		self.right_footer.grid_columnconfigure(0, weight=1)

	def recreate_right_frame(self):
		self.detail_header.destroy()
		self.detail_update_content.destroy()
		self.detail_update_footer.destroy()

		#RECREATE HEADER
		self.create_detail_right_header()

		#RECREATE CONTENT
		self.create_detail_right_content()

		#RECREATE FOOTER
		self.create_detail_right_footer()


	def recreate_right_frame_after_delete(self):

		self.detail_header.destroy()
		self.detail_content.destroy()
		self.detail_footer.destroy()

		#RECREATE HEADER
		self.create_detail_right_header()

		#RECREATE CONTENT
		self.create_detail_right_content()

		#RECREATE FOOTER
		self.create_detail_right_footer()

	def recreate_right_frame_after_add_new(self):
		self.detail_add_new_header.destroy()
		self.detail_add_new_content.destroy()
		self.detail_add_new_footer.destroy()

		#RECREATE HEADER
		self.create_detail_right_header()

		#RECREATE CONTENT
		self.create_detail_right_content()

		#RECREATE FOOTER
		self.create_detail_right_footer()

	def clicked_update_btn(self):
		self.update_mode = True
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_content.destroy()
		self.detail_footer.destroy()

		self.detail_update_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_update_content.grid(row=0, column=0, sticky="nsew")

		for kodeProduct, info in self.current_product.items():
			info = [
				['Kode Produk :', kodeProduct],
				['Nama Produk :', info['produk']],
				['Harga :', info['harga']],
				['Jumlah :', info['jumlah']],
				['Lokasi :', info['lokasi']]
			]
		self.table_info = []
		self.entry_update_product_vars = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
		rows, columns = len(info), len(info[0]) # 3, 2
		for row in range(rows):
			aRow = []
			for column in range(columns):
				if column == 0:
					label = tk.Label(self.detail_update_content, text=info[row][column], font=("Arial", 12), bg="white")
					sticky = "e"
					aRow.append(label)
					label.grid(row=row, column=column, sticky=sticky)
				else:
					entry = tk.Entry(self.detail_update_content, font=("Arial", 12), bg="white", textvariable=self.entry_update_product_vars[row])
					entry.insert(0, info[row][column])
					sticky = "w"
					aRow.append(entry)
					entry.grid(row=row, column=column, sticky=sticky)
			self.table_info.append(aRow)

		self.right_content.grid_rowconfigure(0, weight=1)
		self.right_content.grid_columnconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.detail_update_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_update_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Save', 'Cancel']
		commands = [self.clicked_save_product_btn, self.clicked_cancel_product_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_update_footer, text=feature, bg="white", fg="black", bd=0, font=("Arial", 12, "bold"), command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20)
			self.buttons_features.append(button)

		self.right_footer.grid_rowconfigure(0, weight=1)
		self.right_footer.grid_columnconfigure(0, weight=1)


	def clicked_delete_btn(self):
		self.update_mode = True
		#print(self.last_current_product_index)

		confirm = msg.askyesnocancel('productapp Delete Confirmation', 'Are you sure to delete this product ?')
		index  = self.last_current_product_index
		if confirm:
			self.settings.products.pop(index)
			self.settings.save_data_to_json()
			self.last_current_product_index = 0
			self.current_product = self.settings.products[self.last_current_product_index]

			self.recreate_right_frame_after_delete()
			self.show_all_product_in_listbox()

		self.update_mode = False

	def clicked_add_new_btn(self):
		self.update_mode = True

		self.detail_header.destroy()
		self.detail_content.destroy()
		self.detail_footer.destroy()

		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_add_new_header = tk.Frame(self.right_header, width=frame_w, height=frame_h, bg="green")
		self.detail_add_new_header.grid(row=0, column=0, sticky="nsew")

		self.virt_img = tk.PhotoImage(width=1, height=1)
		self.add_new_label = tk.Label(self.detail_add_new_header, text="Tambah Produk Baru", font=("Arial", 30), width=frame_w, height=frame_h, image=self.virt_img, compound='c', bg="white")
		self.add_new_label.pack()

		self.right_header.grid_rowconfigure(0, weight=1)
		self.right_header.grid_columnconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4

		self.detail_add_new_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_add_new_content.grid(row=0, column=0, sticky="nsew")

		info = [
			['Nama Produk :', None]	,	
			['Kode Produk :', None],
			['Harga :', None,],
			['Jumlah :', None],
			['Lokasi :', None]
		]
		self.table_info = []
		self.entry_update_product_vars = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
		rows, columns = len(info), len(info[0]) # 3, 2
		for row in range(rows):
			aRow = []
			for column in range(columns):
				if column == 0:
					label = tk.Label(self.detail_add_new_content, text=info[row][column], font=("Arial", 12), bg="white")
					sticky = "e"
					aRow.append(label)
					label.grid(row=row, column=column, sticky=sticky)
				else:
					entry = tk.Entry(self.detail_add_new_content, font=("Arial", 12), bg="white", textvariable=self.entry_update_product_vars[row])
					sticky = "w"
					aRow.append(entry)
					entry.grid(row=row, column=column, sticky=sticky)
			self.table_info.append(aRow)


		self.right_content.grid_rowconfigure(0, weight=1)
		self.right_content.grid_columnconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.detail_add_new_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_add_new_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Save', 'Cancel']
		commands = [self.clicked_save_add_new_product_btn, self.clicked_cancel_add_new_product_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_add_new_footer, text=feature, bg="white", fg="black", bd=0, font=("Arial", 12, "bold"), command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20)
			self.buttons_features.append(button)

		self.right_footer.grid_rowconfigure(0, weight=1)
		self.right_footer.grid_columnconfigure(0, weight=1)


	def clicked_save_product_btn(self):
		self.update_mode = False

		confirm = msg.askyesnocancel('productapp Save Confirmation', 'Are you sure to update this product ?')
		
		index = self.last_current_product_index
		if confirm:
			produk = self.entry_update_product_vars[1].get()
			kode = self.entry_update_product_vars[0].get()
			harga = self.entry_update_product_vars[2].get()
			jumlah = self.entry_update_product_vars[3].get()
			lokasi = self.entry_update_product_vars[4].get()
			self.settings.products[index] = {
				kode : {
					"produk" : produk,
					"harga" : harga,
					"jumlah" : jumlah,
					"lokasi" : lokasi
				}
			}
			self.settings.save_data_to_json()
		self.current_product = self.settings.products[index]

		self.recreate_right_frame()

		self.products_list_box.delete(0, 'end')
		self.show_list_products_in_listbox()


	def clicked_cancel_product_btn(self):
		self.update_mode = False

		self.recreate_right_frame()


	def clicked_search_btn(self):

		item_search = self.entry_search_var.get()
		if item_search:
			products = self.settings.products
			self.products_index = []
			index_counter = 0
			for product in products:
				for kodeProduct, info in product.items():
					if item_search in kodeProduct:
						print(kodeProduct)
						self.products_index.append(index_counter)
					elif item_search in info['produk']:
						print(info['produk'])
						self.products_index.append(index_counter)
				index_counter += 1
			print(self.products_index)
			self.products_list_box.delete(0, 'end')
			self.show_list_products_in_listbox()
		else:
			self.show_all_product_in_listbox()


	def clicked_save_add_new_product_btn(self):
		self.update_mode = False

		confirm = msg.askyesnocancel('productapp Save Confirmation', 'Are you sure to add this product ?')
		
		if confirm:
			produk = self.entry_update_product_vars[0].get()
			kode = self.entry_update_product_vars[1].get()
			harga = self.entry_update_product_vars[2].get()
			jumlah = self.entry_update_product_vars[3].get()
			lokasi = self.entry_update_product_vars[4].get()
			new_product= {
				kode : {
					"produk" : produk,
					"harga" : harga,
					"jumlah" : jumlah,
					"lokasi" : lokasi
				}
			}
			self.settings.products.append(new_product)
			self.settings.save_data_to_json()
		index = len(self.settings.products)-1
		self.last_current_product_index = index
		self.current_product = self.settings.products[self.last_current_product_index]

		self.recreate_right_frame_after_add_new()

		self.products_list_box.delete(0, 'end')
		self.show_all_product_in_listbox()



	def clicked_cancel_add_new_product_btn(self):
		self.update_mode = False
		self.recreate_right_frame_after_add_new()











