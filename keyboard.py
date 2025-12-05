from telethon import Button
import re

def start():
    
    buttons = [
        [Button.text("Get File 📤",resize=True)],
        [Button.text("Number List 📜",resize=True),Button.text("Start ♻️",resize=True)],
        [Button.text("All Info 📑",resize=True),Button.text("Delete File ⭕️",resize=True)]
        
    ]
    return buttons

def Cancelgetfile():
    
    buttons = [
        
        [Button.inline("Cancel ❌","Cancel")]
        
        ]
    
    return buttons

def deletefile(files: list):

    buttons = []

    if not files:
        
        return buttons  

    for f in files:
        path = f.value if hasattr(f, "value") else str(f)

        match = re.search(r'([^/\\]+)$', path)
        filename = match.group(1) if match else path

        buttons.append(
            [Button.inline(f"Delete {filename} ⭕️", f"delete_{filename}")]
        )
    buttons.append([Button.inline("Cancel ❌", b"Cancel")])

    return buttons

def getcode(number):
    
    buttons = [
        
        [Button.inline("Get code 🔍",f"code_{number}")],
        [Button.inline("Next 🔜",f"next_{number}")],
        [Button.inline("Cancel ❌", b"Cancel")]
        
        
        ]
    
    return buttons
def nextkey(number):
    
    buttons = [
        
        [Button.inline("Next 🔜",f"next_{number}")],
        [Button.inline("Cancel ❌", b"Cancel")]
        
        
        ]
    
    return buttons


def getautocode(number):
    
    buttons = [
        
        [Button.inline("Again code 🔍",f"code_{number}")],
        [Button.inline("Next 🔜",f"next_{number}"),Button.inline("Email 📧",f"email_{number}")],
        [Button.inline("Cancel ❌", b"Cancel")]
        
        
        ]
    
    return buttons

def numberstatus(number):
    
    buttons = [
        [Button.inline("Accepted ✅",f"Accepted_{number}")],
        [Button.inline("Ban ⭕️",f"Ban_{number}"),Button.inline("Other ➡️",f"Other_{number}")],
        [Button.inline("Cancel ❌", b"Cancel")]
        
        ]
    
    return buttons

def key_log_numbers(log,page=1, page_size=10):


    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_page_data = log[start_index:end_index]

    keyboard = [[
        Button.inline("Number ⚪️", b"ShowAlert"),
        Button.inline("Name 📝", b"ShowAlert"),
        Button.inline("Email 📝", b"ShowAlert"),
        Button.inline("Code 🔢", b"ShowAlert"),
        Button.inline("Delete ❌", b"ShowAlert")
    ]]

    for entry in current_page_data:
        keyboard.append([
            Button.inline(str(entry.number), f"Alert_{entry.number}".encode()),
            Button.inline(str(entry.name), f"Alert_{entry.name}".encode()),
            Button.inline(str(entry.email), f"Alert_{entry.email}".encode()),
            Button.inline(str(entry.code), f"Alert_{entry.code}".encode()),
            Button.inline("❌", f"remove_{entry.number}".encode())
        ])

    navigation_buttons = []
    if start_index > 0:
        navigation_buttons.append(Button.inline("⏪ Last page", f"page_{page - 1}".encode()))
    if end_index < len(log):
        navigation_buttons.append(Button.inline("⏩ Next page", f"page_{page + 1}".encode()))

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    keyboard.append([Button.inline("Cancel ❌", b"Cancel")])

    return keyboard

def key_numbers(numbers, page=1, page_size=10):
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_page_data = numbers[start_index:end_index]

    keyboard = [[Button.inline("Number ⚪️", b"ShowAlert")]]

    for entry in current_page_data:
        keyboard.append([Button.inline(str(entry.number), f"Alert_{entry.number}".encode())])

    navigation_buttons = []
    if start_index > 0:
        navigation_buttons.append(Button.inline("⏪ Last page", f"safe_{page - 1}".encode()))
    if end_index < len(numbers):
        navigation_buttons.append(Button.inline("⏩ Next page", f"safe_{page + 1}".encode()))

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    keyboard.append([Button.inline("Cancel ❌", b"Cancel")])

    return keyboard
