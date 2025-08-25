import json
import os
import re

with open(os.path.join(os.path.dirname(__file__), "error_fixes.json"), "r", encoding="utf-8") as f:
    error_fixes = json.load(f)

def get_fix(text):
    text = text.lower()

    # ac crash + csp detection
    if "unfortunately, assetto corsa has crashed" in text:
        fix = "Please follow: <#1365257112372117514>. Uploading the crash report or log.txt (`/Documents/Assetto Corsa/logs/`) will help narrow down your exact issue.\n"
        
        version_match = re.search(r"\b0\.\d+\.\d+(?:-[\w\d]+)?\b", text)
        if version_match:
            version = version_match.group()
            fix += f"\nDetected CSP version: `{version}`"

            if "preview" in version:
                if "0.2.8" in fix:     
                    fix += "\n**Warning:** Preview builds of CSP may be unstable and require more performance."
                else:
                    fix += "\n**Warning:** Preview builds of CSP may be unstable and require more performance. Currently the most stable preview CSP version is: 0.2.8 preview."

            elif version == "0.2.7" or "0.2.9":
                fix += "\nStay on either 0.2.7 or 0.2.9 CSP are currently the most reliable CSP versions."

            else:
                fix += "\nSwitching to 0.2.7 or 0.2.9 CSP may help, as these are the most reliable CSP versions."
        return "**Error Found:** `unfortunately, assetto corsa has crashed`\n\n" + fix

    # handshake
    if "handshake failed" in text:
        if "server auth failed:prohibited username" in text or "server auth failed: prohibited username" in text:
            fix = "You will need to change or disable your online name in Content Manager.\nOpen Content Manager -> Settings -> Content Manager > Drive > Online Name."
            return "**Error Found:** `prohibited username`\n\n" + fix
        elif "server auth failed: you are not whitelisted on this server" in text:
            fix = "Please connect your steam ID using <#1000157728737599691>. Whitelisting may take up to 10 minutes to take affect. If you are trying to join VIP servers, ensure you have the correct tiered subscription."
            return "**Error Found:** `you are not whitelisted on this server`\n\n" + fix
        else:
            fix = "Please follow all 12 steps in: <#1322243958419750942> until the issue is fixed. The bottom left of the loading screen, may say exactly what your issue is when the game crashes."
            return "**Error Found:** `handshake failed`\n\n" + fix

    # srp / missing cars / dwrite dll is missing
    if "is missing" in text or "custom shaders patch is required" in text:
        fix = "" 

        if "shuto_revival_project_beta/main_layout" in text:
            fix += "\n\nYou will need to install the SRP track manually following: <#1322236089083105343>"
        if "nohesi_415" in text and "is missing" in text:
            fix+= "\n\nYou can install the 415 track by pressing `install missing content`: <#1322223184367587462>"
        if "custom shaders patch is required" in text:
            fix += "You will need to install Custom Shaders Patch. To do so, open Content Manager -> settings -> CSP -> about & updates. Or install it manually: <#1322225183297376266>"
        if "car" in text and "is missing" in text:
            fix += "\n\nYou can install the missing cars by pressing `install missing content`:<#1322223184367587462>"
        if "main patch file" in text and "is missing in ac root folder (reinstall patch)." in text:
            fix += "\n\nYour current CSP patch is damaged. Please reinstall it by following: <#1322240298210033804>"
            return "**Error Found:** `dwrite.dll is missing`" + fix
        return "**Error Found:** `missing content`" + fix

    # backed does not respond/ loading chat
    if "loading chat" in text or "backed does not respond" in text or "backend does not respond" in text:
        fix = ""
        
        if "backed does not respond" in text:
            fix += "Please do: <#1376100478051684443>"
            return "**Error Found:** `backed does not respond`\n" + fix
        elif "backend does not respond" in text:
            fix += "Please do: <#1376100478051684443>"
            return "**Error Found:** `backed does not respond`\n" + fix
        elif "loading chat" in text and "please wait" in text:
            fix += "Please do: <#1376100478051684443>"
            return "**Error Found:** `loading chat please wait`\n" + fix
        
    # csp installation is damaged / version mismatch
    if "csp installation is damaged" in text:
        fix = "A mismatch of your CSP version, is usually fixed by restarting your pc. If that does nothing, please do: <#1322240298210033804>\n"
        
        version_match = re.search(r"\b0\.\d+\.\d+(?:-[\w\d]+)?\b", text)
        if version_match:
            version = version_match.group()
            fix += f"\nDetected CSP version: `{version}`"

            if "0.2.7" not in version or "0.2.9" not in version or "0.2.11" not in version :
                fix += "\nPlease also ensure you have 0.2.7/0.2.9/0.2.11 csp installed. These are the csp versions recommended for our servers."
        return "**Error Found:** `csp installation is damaged`\n\n" + fix        
        
    # fallback for normal errors
    for error, fix in error_fixes.items():
        if error.lower() in text:
            return f"**Error Found:** `{error}`\n{fix}"

    return None


