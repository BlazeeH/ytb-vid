import tkinter as tk

# Create the main window
root = tk.Tk()
root.geometry("400x250")  # Set window size
root.title("Welcome to My App")  # Set window title

# Create a StringVar to associate with the label
text_var = tk.StringVar()
text_var.set("Hello, World!")

# Create the label widget with all options
label = tk.Label(root, 
                 textvariable=text_var, 
                 anchor=tk.W,       
                 bg="lightblue",      
                 height=1,              
                 width=30,              
                 bd=3,                  
                 font=("Arial", 16, "bold"), 
                 cursor="hand2",   
                 fg="red",             
                 padx=1,               
                 pady=1,                
                 justify=tk.CENTER,    
                 relief=tk.RAISED,     
                 underline=0,           
                 wraplength=250         
                )

# Pack the label into the window
label.pack(pady=20)  # Add some padding to the top


# Run the main event loop
root.mainloop()