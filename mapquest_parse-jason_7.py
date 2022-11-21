import urllib.parse
import requests
import PySimpleGUI as sg

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "hWmoxgA3H7M7HOGZe2P51HUPcLVKXNdw"

sg.theme('DarkAmber')   # Add a touch of color
# Content of the Window
layout = [  [sg.Text('Input Starting Location'), sg.InputText()],
            [sg.Text('Input Destination'), sg.InputText()],
            [sg.Text('[1]KM or [2]Mi'), sg.InputText()],
            [sg.Button('Continue'), sg.Button('Exit')] ]

# Creating the Window
window = sg.Window('Window Title', layout)

# Event Loop to process events and get the values of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': # if the user closes the GUI or presses "Exit" button
        break
    else:
        orig = values[0]
        dest = values[1]
        dist = values[2]
        url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest})
        json_data = requests.get(url).json()
        print("URL: " + (url) + "\n")
        print("Brought to you by THE BOYS:\nAlexis Alfonso\nAris Manengyao\nDan Bautista\nRonald Soriano\n")

        json_status = json_data["info"]["statuscode"]
        if json_status == 0:
            print("API Status: " + str(json_status) + " = A successful route call.\n")
            print("Directions from: " + (orig) + " to " + (dest) + "\n")
            print("Trip Duration:   " + (json_data["route"]["formattedTime"]) + "\n")
            if dist == 1:
                print("Kilometers:   " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)) + "\n")
            if dist == 2:
                print("Miles:   " + str("{:.2f}".format((json_data["route"]["distance"]))) + "\n")
                print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)) + "\n")
            for each in json_data["route"]["legs"][0]["maneuvers"]:
                print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)") + "\n")

        elif json_status == 402:
            print("*************************************************")
            print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
            print("*************************************************\n")
        elif json_status == 611:
            print("*************************************************")
            print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
            print("*************************************************\n")
        else:
            print("*************************************************")
            print("For Status Code: " + str(json_status) + "; Refer to:")
            print("https://developer.mapquest.com/documentation/directions=api/status=codes")
            print("*************************************************\n")
window.close()
