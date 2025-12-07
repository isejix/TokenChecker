from telethon import *
from telethon import TelegramClient, events
import configparser
import socks
import keyboard
from Domain.Repository import StepRepo, ReceivedNumbersRepo, CachRepo ,LogNumberRepo
from Domain.DB import Database
import re
import os
import aiohttp
import asyncio
import random
import time
running_tasks = {}

Config = configparser.ConfigParser()
Config.read("./confing.ini")
api_id = Config.get("Info", "api_id")
api_hash = Config.get("Info", "api_hash")
bot_token = Config.get("Info", "bot_token")

# proxy = (socks.SOCKS5, '127.0.0.1', 2080)
Client = TelegramClient("TokenChecker", api_id=int(api_id), api_hash=str(api_hash))

def is_sudo(chatid):
    
    sudo = Config.get("Info", "sudo") 
    
    sudo_list = [int(x.strip()) for x in sudo.split(",")]  
    
    return chatid in sudo_list

@Client.on(events.NewMessage)
async def Onmessege(m):

    chatid = m.sender.id

    is_step = await StepRepo.has_step(chatid)
    
    text = m.raw_text
    
    if text == "/start":
        
        key = keyboard.start()
        
        await m.respond("Wellcome to Token Checker Bot 🤖\n\nThank for using our bot 🙏🏻",buttons = key)
        
    elif text == "Get File 📤":
        
        key = keyboard.Cancelgetfile()
        
        await m.respond("Send Token file to loading the numbers and links... 📨",buttons = key)
        
        await StepRepo.create_step(chatid,"GetFile")
    
    elif text == "Number List 📜":
        
        numbers = await ReceivedNumbersRepo.get_all_numbers()
        
        if not numbers:
            
            await m.respond("❌ No numbers found!")
            
            return       
        
        path = numbers[0].path if numbers[0].path else "Unknown"
        
        match = re.search(r'([^/\\]+)$', path)
        
        filename = match.group(1) if match else path

        key = keyboard.key_numbers(numbers)
        
        await m.respond(f"List of number from {filename} file 📑",buttons = key)
        
    elif text == "Start ♻️":
        
        number = await ReceivedNumbersRepo.get_number_by_id(1)
        
        if not number:
            
            await m.respond("There is no Number ❗️")
            
        number = number.number
        
        isvalid = await LogNumberRepo.get_log_number_by_number(number)
        
        if isvalid is None:

            link = await ReceivedNumbersRepo.get_number_by_phone(number)
                
            link = link.link
                
            isany = await CachRepo.get_user_cache_value(chatid,"number")
                
            if isany is None:
                
                await CachRepo.create_Cach(chatid,"number",number)
                
            await CachRepo.update_user_cache_value(chatid,"number",number)
                
                # await m.answer("Checking code... ⏳") 
                
            key = keyboard.getcode(number)
                
            messege = await m.respond(f"Number 📱: {number}",buttons = key)

            task = start_check(chatid=chatid,link=link)
            
            code = await task
                
            if code is not None:
                    
                await messege.delete()
                    
                await ReceivedNumbersRepo.update_status_by_number(number,ReceivedNumbersRepo.SessionStatus.Accepted)
                    
                key = keyboard.getautocode(number)
                    
                with open("name.txt", "r", encoding="utf-8") as f:
                        
                    content = f.read()

                names = [name.strip() for name in content.split(",") if name.strip()]

                random_name = random.choice(names)
                    
                await CachRepo.create_Cach(chatid,"name",random_name)
                    
                isany = await CachRepo.get_user_cache_value(chatid,"code")
                    
                if isany is None:
                    
                    await CachRepo.create_Cach(chatid,"code",code)
                    
                await CachRepo.update_user_cache_value(chatid,"code",code)
                    
                await LogNumberRepo.create_log_number(number=number,code=code,name=random_name,link=link)
                    
                await m.respond(f"Number 📱: {number}\nCode 🔑: {code}\nFull name 📄: {random_name}",buttons = key)
        
        else:
            
            await m.respond(f"The number {number} is already exsist ⚠️")
            
            link = await ReceivedNumbersRepo.get_number_by_phone(number)
                
            link = link.link
                
            isany = await CachRepo.get_user_cache_value(chatid,"number")
                
            if isany is None:
                
                await CachRepo.create_Cach(chatid,"number",number)
                
            await CachRepo.update_user_cache_value(chatid,"number",number)
                
                # await m.answer("Checking code... ⏳") 
                
            key = keyboard.getcode(number)
                
            messege = await m.respond(f"Number 📱: {number}",buttons = key)

            task = start_check(chatid=chatid,link=link)
            
            code = await task
                
            if code is not None:
                
                await messege.delete()
                    
                await ReceivedNumbersRepo.update_status_by_number(number,ReceivedNumbersRepo.SessionStatus.Accepted)
                    
                key = keyboard.getautocode(number)
                    
                isany = await CachRepo.get_user_cache_value(chatid,"code")
                    
                if isany is None:
                    
                    await CachRepo.create_Cach(chatid,"code",code)
                    
                await CachRepo.update_user_cache_value(chatid,"code",code)
                
                name = await LogNumberRepo.get_name_by_number(number)
                    
                await LogNumberRepo.update_log_number(number=number,code=code,name=name)
                    
                await m.respond(f"Number 📱: {number}\nCode 🔑: {code}\nFull name 📄: {name}",buttons = key)
                
            
    elif text == "Delete File ⭕️":
        
        all_numbers = await ReceivedNumbersRepo.get_all_numbers() 
        
        paths = set() 
        
        for num in all_numbers:
        
            if num.path:
        
                paths.add(num.path)
        
        key = keyboard.deletefile(list(paths))
        
        if not key:
            
            await m.respond("❌ No files found to delete.")
  
            return
        
        await m.respond("List of File loaded for delete file and numbers from database⭕️",buttons = key)
            
    elif text == "All Info 📑":
        
        numbers = await LogNumberRepo.get_all_log_numbers()

        key = keyboard.key_log_numbers(numbers)
        
        await m.respond("This is the numbers info ℹ️",buttons = key)
        
    elif is_step:
        
        step = await StepRepo.get_step(chatid)
        
        step = step.step
        
        if step == "GetFile":
            
            if m.document and m.file.name.endswith(".txt"):
                
                os.makedirs("./downloads", exist_ok=True)
                
                path = f"./downloads/{m.file.name}"
                
                await m.download_media(file=path)
                
                numbers = []
                
                count = 0

                pattern = re.compile(r"(\+?\d+)[^\d]*?(https?://\S+)")

                with open(path, "r") as f:
                    
                    for line in f:
                        
                        line = line.strip()
                        
                        if not line:
                        
                            continue
                        
                        match = pattern.search(line)
                        
                        if match:
                        
                            phone = match.group(1)
                        
                            link = match.group(2)

                            count = count + 1
                            
                            numbers.append({
                                "phone": phone,
                                "link": link
                            })
                        
                        else:
                        
                            print(f"⚠️ Could not parse line: {line}")

                already_saved_numbers = []
                
                new_numbers = []

                for item in numbers:
                
                    phone = item["phone"]
                
                    if not phone.startswith("+"):
                
                        phone = "+" + phone
                    
                    valid = await ReceivedNumbersRepo.get_number_by_phone(phone)
                    
                    if valid is not None:
                
                        already_saved_numbers.append(f"{phone} → {item['link']}")
                
                        continue

                    await ReceivedNumbersRepo.create_number(phone, item["link"],path,ReceivedNumbersRepo.SessionStatus.Pending)
                
                    new_numbers.append(f"{phone} → {item['link']}")

                path_old = os.path.abspath("./downloads/already_saved.txt")
                path_new = os.path.abspath("./downloads/new_saved.txt")

                if already_saved_numbers:
                    with open(path_old, "w", encoding="utf-8") as f:
                        f.write(f"{len(already_saved_numbers)} numbers already exist ❗️\n\n")
                        for line in already_saved_numbers:
                            f.write(line + "\n")

                if new_numbers:
                    with open(path_new, "w", encoding="utf-8") as f:
                        f.write(f"Saved {len(new_numbers)} numbers successfully ✅\n\n")
                        for line in new_numbers:
                            f.write(line + "\n")

                if already_saved_numbers:
                
                    await m.reply("Numbers already in database ⬇️", file=path_old)
                
                if new_numbers:
                
                    await m.reply("Newly saved numbers ⬇️", file=path_new)
                    
                asyncio.create_task(delete_later([path, path_old, path_new]))
                
                await StepRepo.delete_step(chatid)
            
            else:
                
                await m.reply("The input is not valid ❌\n\nPlease send .txt file 🙏🏻")
                
                return

        elif step == "sendemail":
            
            email = text.strip()
            
            emailre = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
            
            if not emailre.match(email):
                
                await m.respond("❌ Email is not valid. Please send a correct email ")
                
                return
            
            await StepRepo.delete_step(chatid)

            name = await CachRepo.get_user_cache_value(chatid,"name")
                        
            number = await CachRepo.get_user_cache_value(chatid,"number")
            
            code = await CachRepo.get_user_cache_value(chatid,"code")
            
            await LogNumberRepo.update_log_number(number,email,code,name)
            
            if not number.startswith("+"):
                
                number = "+" + number
                        
            key = keyboard.nextkey(number)
            
            await m.respond(f"Number: {number}\nCode: {code}\nEmail: {email}\nFull name: {name}",buttons = key) 
            

@Client.on(events.CallbackQuery)
async def callbacks(m):
    
    chatid = m.sender.id
    
    data = m.data.decode()
    
    if "code_" in data:
        
        number = data.replace("code_","")
        
        isvalid = await LogNumberRepo.get_log_number_by_number(number)
        
        if isvalid is None:
        
            link = await ReceivedNumbersRepo.get_number_by_phone(number)
        
            link = link.link
            
            await m.answer("Checking code... ⏳") 


            task = start_check(chatid=chatid,link=link)
            
            code = await task
            
            if code:
                
                await ReceivedNumbersRepo.update_status_by_number(number,ReceivedNumbersRepo.SessionStatus.Accepted)
                
                isany = await CachRepo.get_user_cache_value(chatid,"code")
                
                if isany is None:
                
                    await CachRepo.create_Cach(chatid,"code",code)
                
                await CachRepo.update_user_cache_value(chatid,"code",code)
                
                await ReceivedNumbersRepo.update_status_by_number(number,ReceivedNumbersRepo.SessionStatus.Accepted)
                
                key = keyboard.getautocode(number)
                
                name = await CachRepo.get_user_cache_value(chatid,"name")
                
                await LogNumberRepo.create_log_number(number=number,code=code,name=name,link=link)
                
                await m.delete()
                
                await m.respond(f"Number 📱: {number}\nCode 🔑: {code}\nFull name 📄: {name}",buttons = key)
                
            
        else:
            
            await m.respond(f"The number {number} is already exsist ⚠️")
            
            link = await ReceivedNumbersRepo.get_number_by_phone(number)
                
            link = link.link
                
            isany = await CachRepo.get_user_cache_value(chatid,"number")
                
            if isany is None:
                
                await CachRepo.create_Cach(chatid,"number",number)
                
            await CachRepo.update_user_cache_value(chatid,"number",number)
                
                # await m.answer("Checking code... ⏳") 
                
            key = keyboard.getcode(number)
                
            messege = await m.respond(f"Number: {number}",buttons = key)

            task = start_check(chatid=chatid,link=link)
            
            code = await task
                
            if code is not None:
                    
                await ReceivedNumbersRepo.update_status_by_number(number,ReceivedNumbersRepo.SessionStatus.Accepted)
                    
                key = keyboard.getautocode(number)
                    
                isany = await CachRepo.get_user_cache_value(chatid,"code")
                
                await messege.delete()
                    
                if isany is None:
                    
                    await CachRepo.create_Cach(chatid,"code",code)
                    
                await CachRepo.update_user_cache_value(chatid,"code",code)
                
                name = await LogNumberRepo.get_name_by_number(number)
                    
                await LogNumberRepo.update_log_number(number=number,code=code,name=name)
                    
                await m.respond(f"Number 📱: {number}\nCode 🔑: {code}\nFull name 📄: {name}",buttons = key)
            
        
    elif "next_" in data:
        
        number = data.replace("next_","")
        
        number = str(number)
        
        print(number)
        
        key = keyboard.numberstatus(number)
        
        await m.edit("Please click your reasen for move to next Token number 🙏🏻",buttons = key)

    elif "Ban_" in data:
        
        number = data.replace("Ban_","")
        
        next = await ReceivedNumbersRepo.get_number_by_phone(number)
        
        await ReceivedNumbersRepo.update_status_by_number(number,ReceivedNumbersRepo.SessionStatus.Ban)
        
        key = keyboard.numberstatus(number)
        
        lastn = await ReceivedNumbersRepo.get_last_number()
        
        lastn = lastn.id

        id = next.id
        
        id += 1
        
        if id <= lastn:
            
            number = await ReceivedNumbersRepo.get_number_by_id(id)
            
            number = number.number

            key = keyboard.getcode(number)

            await m.edit(f"{number}", buttons=key)
            
        else:
            
            await m.edit("There is no more number for getting code ❗️")
    
    elif "Accepted_" in data:
        
        number = data.replace("Accepted_","")
        
        next = await ReceivedNumbersRepo.get_number_by_phone(number)
        
        await ReceivedNumbersRepo.update_status_by_number(number,ReceivedNumbersRepo.SessionStatus.Accepted)
        
        key = keyboard.numberstatus(number)
        
        lastn = await ReceivedNumbersRepo.get_last_number()
        
        lastn = lastn.id

        id = next.id
        
        id += 1
        
        if id <= lastn:
            
            number = await ReceivedNumbersRepo.get_number_by_id(id)
            
            number = number.number

            key = keyboard.getcode(number)

            await m.edit(f"{number}", buttons=key)
            
            await CachRepo.delete_all_Cach_by_chatid(chatid)
            
            await StepRepo.delete_step(chatid)
            
        else:
            
            await m.edit("There is no more number for getting code ❗️")
    
    elif "Other_" in data:
        
        number = data.replace("Other_","")
        
        next = await ReceivedNumbersRepo.get_number_by_phone(number)
        
        await ReceivedNumbersRepo.update_status_by_number(number,ReceivedNumbersRepo.SessionStatus.Other)
        
        key = keyboard.numberstatus(number)
        
        lastn = await ReceivedNumbersRepo.get_last_number()
        
        lastn = lastn.id

        id = next.id
        
        id += 1
        
        if id <= lastn:
            
            number = await ReceivedNumbersRepo.get_number_by_id(id)
            
            number = number.number

            key = keyboard.getcode(number)

            await m.edit(f"{number}", buttons=key)
            
        else:
            
            await m.edit("There is no more number for getting code ❗️")

    elif "delete_" in data:
        
        path = data.replace("delete_","")
        
        path = "./downloads/" + path
        
        await ReceivedNumbersRepo.delete_all_numbers_by_path(path)
        
        all_numbers = await ReceivedNumbersRepo.get_all_numbers() 
        
        paths = set() 
        
        for num in all_numbers:
        
            if num.path:
        
                paths.add(num.path)
        
        key = keyboard.deletefile(list(paths))
        
        if key:
        
            await m.edit("List of File loaded for delete file and numbers from database⭕️",buttons = key)
            
        else:
            
            await m.edit("No files remaining to delete ❗️")

    elif "Cancel" in data:
        
        ischach =await CachRepo.has_any_cache(chatid)
        
        if ischach:
            
            await CachRepo.delete_all_Cach_by_chatid(chatid)
        
        isstep = await StepRepo.has_step(chatid)
        
        if isstep:
            
            await StepRepo.delete_step(chatid)
            
        if running_tasks is not None:

            cancel_check(chatid)
            
        key = keyboard.start()
        
        await m.edit("The proccess was seccessfuly canceled ✅",buttons = key)
        
    elif "ShowAlert" in data:
        
        await m.answer("This button is for display purposes only ❤️", alert=True)
        
    elif "Alert_" in data:
        
        alert = data.replace("Alert_","")
        
        await m.answer(f"{alert}") 

    elif "email_" in data:
        
        number = data.replace("email_","")
        
        await m.edit("Please send email 🙏🏻")
            
        # await CachRepo.get_user_cache_value(chatid,"code",code)
        
        # await CachRepo.get_user_cache_value(chatid,"number",number)
            
        await StepRepo.create_step(chatid,"sendemail")
    
    elif "remove_" in data:
        
        number = data.replace("remove_","")
        
        await LogNumberRepo.delete_log_number(number)

        numbers = await LogNumberRepo.get_all_log_numbers()

        key = keyboard.key_log_numbers(numbers)
        
        await m.delete()
        
        await m.respond("This is the numbers info ℹ️",buttons = key)  
        
    elif "page_" in data:
        
        page = int(data.split("_")[1]) 
        
        numbers = await LogNumberRepo.get_all_log_numbers()

        if not numbers:
        
            await m.answer("There is no data to show ❗️", show_alert=True)
        
            return
        
        key = keyboard.key_log_numbers(numbers,page=page)
        
        await m.edit(f"ALL info Tokens number page({page}) 📜", buttons=key)
        
    elif "safe_" in data:
                
        page = int(data.split("_")[1]) 
        
        numbers = await ReceivedNumbersRepo.get_all_numbers()
        
        if not numbers:
            
            await m.answer("There is no data to show ❗️", show_alert=True)

            return       

        key = keyboard.key_numbers(numbers,page=page)
        
        path = numbers[0].path if numbers[0].path else "Unknown"
        
        match = re.search(r'([^/\\]+)$', path)
        
        filename = match.group(1) if match else path
        
        await m.edit(f"List of number from {filename} file 📑\npage({page})", buttons=key)
        

      
async def check_code(chatid: int, link: str, duration: int = 300, interval: float = 2.0):
    code_pattern = re.compile(r"\b\d{5}\b")
    end_time = asyncio.get_event_loop().time() + duration

    try:
        async with aiohttp.ClientSession() as session:
            while asyncio.get_event_loop().time() < end_time:
                if running_tasks.get(chatid) is None:
                    print(f"Task for chat {chatid} cancelled")
                    return None

                try:
                    async with session.get(link, timeout=10) as resp:
                        text = await resp.text()
                        match = code_pattern.search(text)
                        if match:
                            code = match.group()
                            print(f"✅ CODE FOUND: {code}")
                            return code
                except Exception as e:
                    print("❌ ERROR:", e)

                await asyncio.sleep(interval)

    except asyncio.CancelledError:
        print(f"Task for chat {chatid} cancelled by asyncio")
        return None

    print("❌ No code found within the time limit")
    return None

def start_check(chatid: int, link: str):
    task = asyncio.create_task(check_code(chatid, link))
    running_tasks[chatid] = task
    return task

def cancel_check(chatid: int):
    task = running_tasks.pop(chatid, None)
    if task:
        task.cancel()

async def delete_later(files):
    await asyncio.sleep(2)
    for f in files:
        if os.path.exists(f):
            os.remove(f)

async def run(): 
    await Database.init_db()
    
    await Client.start(bot_token=bot_token)
    
    print("Bot is running...")
    
    await Client.run_until_disconnected()
 

Client.loop.run_until_complete(run())