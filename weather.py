import tkinter as tk
import requests
from tkinter.constants import LEFT


def format_response(weather):
    try:
        place = (
            weather["location"]["name"]  # city
            + ", "
            + weather["location"]["country"]  # country
        )

        # If the key "forecast" exist, the request was 3 days forecast
        if "forecast" in weather:
            response = place
            for days in weather["forecast"]["forecastday"]:
                response += f"\n\nDate: {days['date']} \nCondition: {days['day']['condition']['text']} \nTemp. Max.: {days['day']['maxtemp_c']} \nTemp. Max.: {days['day']['mintemp_c']} \nProb. Rain: {days['day']['daily_chance_of_rain']}\n"
        else:
            w = weather["current"]
            response = f"{place} \n\nTemperature (ºC): {w['temp_c']} \nConditions: {w['condition']['text']} \nWind: {w['wind_kph']} Km/h {w['wind_dir']}"
    except:
        response = "The weather information couldn't be found."

    return response


# Execute API
def get_weather(place):
    base_url = "http://api.weatherapi.com/v1"
    api_key = ""  # The api key is generated when you sign up on the website

    if weatherType.get() == 0:
        # daily forecast uri
        url = base_url + "/current.json?key={}&q={}".format(api_key, place)
    else:
        # 3 days forecast uri
        url = base_url + "/forecast.json?key={}&q={}&days=7".format(api_key, place)

    try:
        response = requests.get(url)
        label_msg["text"] = format_response(response.json())
    except:
        label_msg["text"] = "Location isn't found"


root = tk.Tk()
root.title("Weather Forecast")
root.geometry("600x500")
root.configure(background="#4db8ff")

# Define background window
canvas = tk.Canvas(root)
canvas.pack()

# Shows image as background
bg_img = tk.PhotoImage(file="landscape.png")
bg_label = tk.Label(root, image=bg_img)
bg_label.place(relwidth=1, relheight=1)

# Create top frame
top_frame = tk.Frame(root, bg="#4db8ff", bd=5)
top_frame.place(relx=0.5, rely=0.1, relheight=0.15, relwidth=0.75, anchor="n")

# Create input field an place on top frame
input_field = tk.Entry(top_frame, font=("Courier", 18))
input_field.place(relwidth=0.65, relheight=0.5)
input_field.focus()

# Create search button an place on top frame
search_btn = tk.Button(
    top_frame, text="Search", font=40, command=lambda: get_weather(input_field.get())
)
search_btn.place(relx=0.7, relwidth=0.3, relheight=1)

# Select weather forecast
weatherType = tk.IntVar()
tk.Radiobutton(
    top_frame, text="Current weather", variable=weatherType, value=0, bg="#4db8ff"
).place(rely=0.5, relwidth=0.3, relheight=0.5)

tk.Radiobutton(
    top_frame, text="3 days forecast", variable=weatherType, value=1, bg="#4db8ff"
).place(relx=0.35, rely=0.5, relwidth=0.3, relheight=0.5)

# Create bottom frame
bottom_frame = tk.Frame(root, bg="#4db8ff", bd=10)
bottom_frame.place(relx=0.5, rely=0.25, relheight=0.7, relwidth=0.75, anchor="n")

# Create output field an place on bottom frame
label_msg = tk.Label(bottom_frame, font=("Courier", 12), justify=LEFT, anchor="nw")
label_msg.place(relheight=1, relwidth=1)

root.mainloop()
