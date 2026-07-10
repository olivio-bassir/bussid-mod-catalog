#!/usr/bin/env python3
# Telecharge des liveries (webp/jpg) depuis leur CDN, convertit en PNG (le jeu exige PNG),
# les heberge dans liveries_pack/ et ajoute des entrees catalogue (un-clic, groupees par vehicule).
import json, os, io, urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK = os.path.join(ROOT, "liveries_pack")
os.makedirs(PACK, exist_ok=True)
RAW = "https://raw.githubusercontent.com/olivio-bassir/bussid-mod-catalog/main/liveries_pack/"

# (slug, nom affiche, carrosserie/vehicule, auteur, url)
ITEMS = [
 ("jb-sugeng-rahayu-shd","Sugeng Rahayu SHD Ori","Jetbus SHD","dianisa","https://assets.dianisa.com/media/2024/04/23.-Sugeng-Rahayu-SHD-Ori.webp"),
 ("jb-ranau-indah-jb3-shd","Ranau Indah JB3 SHD","Jetbus SHD","dianisa","https://assets.dianisa.com/media/2024/03/70.-Ranau-Indah-JB3-SHD.webp"),
 ("jb-pangeran-arjuna-voyager","Pangeran Arjuna Voyager","Jetbus Voyager","dianisa","https://assets.dianisa.com/media/2024/07/28.-Pangeran-Arjuna-dop-JB3Voyager.webp"),
 ("jb-agra-mas-jb3-tronton","Agra Mas JB3 Tronton","Jetbus 3","dianisa","https://assets.dianisa.com/media/2024/07/2.-Agra-Mas-JB3-tronton-UMP.webp"),
 ("jb-sugeng-rahayu-jb3","Sugeng Rahayu JB3","Jetbus 3","dianisa","https://assets.dianisa.com/media/2024/04/2.-Sugeng-Rahayu-JB3-AE.webp"),
 ("jb-kramat-djati-jb3","Kramat Djati JB3","Jetbus 3","dianisa","https://assets.dianisa.com/media/2024/04/69.-Kramat-Djati-Jb3-MBS.webp"),
 ("jb-new-shantika-jb3","New Shantika JB3","Jetbus 3","MBS","https://assets.dianisa.com/media/2024/04/71.-New-Shantika-Jb3-MBS.webp"),
 ("jb-als-jbhd-vol3","ALS JBHD vol.3","Jetbus HD","Rindray","https://assets.dianisa.com/media/2024/07/5.-ALS-JBHD-vol-3-Rindray-scaled.webp"),
 ("jb-arjuna-samba-hd","Arjuna Samba HD","Jetbus HD","dianisa","https://assets.dianisa.com/media/2024/07/6.-Arjuna-Samba-HD.webp"),
 ("jb-new-mpm-jb2","New MPM JB2 Ori","Jetbus 2","PWJ","https://assets.dianisa.com/media/2024/03/46.-NEW-MPM-JB2-ORI-PWJ.webp"),
 ("jb-eka-jb2hd","EKA JB2HD","Jetbus 2","RSM","https://assets.dianisa.com/media/2024/04/49.-EKA-JB2HD-RSM.webp"),
 ("jb-sinar-jaya-jb1","Sinar Jaya JB1","Jetbus 1","OLD Mans Gaming","https://assets.dianisa.com/media/2024/03/103.-Sinar-Jaya-JB1-OLD-Mans-Gaming.webp"),
 ("jb-budiman-jb1","Budiman JB1","Jetbus 1","OLD Mans Gaming","https://assets.dianisa.com/media/2024/03/96.-Budiman-JB1-OLD-Mans-Gaming.webp"),
 ("jb-sugeng-golden-sdd","Sugeng Rahayu Golden Star SDD","Jetbus SDD","dianisa","https://assets.dianisa.com/media/2024/04/46.-Sugeng-Rahayu-Golden-Star-SDD.webp"),
 ("av-rosalia-d1","Rosalia Indah Avante D1","Avante D1","dianisa","https://assets.dianisa.com/media/2024/07/1.-Rosalia-Indah-Avante-D1.webp"),
 ("av-als-bimasena-d2","ALS Bimasena Avante D2","Avante D2","dianisa","https://assets.dianisa.com/media/2024/03/6.-ALS-Bimasena-SDD-Rombak-Avante-D2.webp"),
 ("av-kencana-d2","Kencana Avante D2","Avante D2","dianisa","https://assets.dianisa.com/media/2024/03/37.-Kencana-SDD-Rombak-Avante-D2.webp"),
 ("av-rosalia-h8","Rosalia Indah Avante H8","Avante H8","dianisa","https://assets.dianisa.com/media/2024/07/10.-Rosalia-Indah-Avante-H8.webp"),
 ("av-als-h9","ALS Avante H9","Avante H9","HF x FCRz","https://assets.dianisa.com/media/2024/03/26.-ALS-Avante-H9-HF-X-FCRz.webp"),
 ("av-als-shd","ALS Avante SHD","Avante SHD","dianisa","https://assets.dianisa.com/media/2024/03/1.-A.L.S-Avante-SHD.webp"),
 ("tk-als-scorpion-king","ALS Scorpion King HD","Tentrem Scorpion King","dianisa","https://assets.dianisa.com/media/2024/03/8.-A.L.S-Scorpion-King-HD.webp"),
 ("dk-draka-inkscape","Draka Inkscape Premium XHD","Draka STJ","dianisa","https://assets.dianisa.com/media/2024/04/9.-Livery-Bus-Draka-Inkscape-Premium-Sudiro-Tungga-Jaya-XHD.webp"),
 ("dk-stj-draka-xhd","STJ Draka XHD","Draka STJ","dianisa","https://assets.dianisa.com/media/2024/04/29.-STJ-Draka-XHD.webp"),
 ("sk-san-skyliner-sdd","SAN Skyliner SDD","Skyliner","dianisa","https://assets.dianisa.com/media/2024/03/74.-SAN-Skyliner-SDD.webp"),
 ("lg-als-prime-xhd","ALS Prime XHD","Legacy SR2 XHD","dianisa","https://assets.dianisa.com/media/2024/03/7.-A.L.S-Prime-XHD.webp"),
 ("lg-agra-mas-xhd","Agra Mas XHD","Legacy SR2 XHD","dianisa","https://assets.dianisa.com/media/2024/04/25.-Agra-Mas-XHD.webp"),
 ("lg-primajasa-xhd","Primajasa XHD","Legacy SR2 XHD","dianisa","https://assets.dianisa.com/media/2024/04/27.-Primajasa-XHD.webp"),
 ("lg-sinar-jaya-xhd","Sinar Jaya XHD","Legacy SR2 XHD","dianisa","https://assets.dianisa.com/media/2024/04/64.-Sinar-Jaya-XHD.webp"),
 ("lg-als-sr2-scania","ALS SR2 Scania","Legacy SR2","dianisa","https://assets.dianisa.com/media/2024/03/48.-ALS-SR2-Scania.webp"),
 ("lg-sinjay-sr2-triple","Sinjay SR2 Triple Axle","Legacy SR2","WSP","https://assets.dianisa.com/media/2024/04/30.-Sinjay-SR2-Triple-Axle-WSP.webp"),
 ("lg-als-sr3-panorama","ALS SR3 Panorama","Legacy SR3","Thien","https://assets.dianisa.com/media/2024/03/50.-ALS-SR3-Panorama-Thien.webp"),
 ("lg-rosalia-sr3","Rosalia Indah SR3","Legacy SR3","MN Art x BFC","https://assets.dianisa.com/media/2024/07/22.-Rosalia-indah-SR3-MN-X-BFC.webp"),
 ("lg-als-discovery","ALS Discovery HD","Laksana Discovery","dianisa","https://assets.dianisa.com/media/2024/03/2.-A.L.S-Discovery-HD.webp"),
 ("lg-laksana-anda-shd","Laksana Anda SHD","Legacy (Old)","dianisa","https://assets.dianisa.com/media/2024/03/69.-Laksana-Anda-SHD.webp"),
 ("sr-era-trans-shd","Era Trans Srikandi SHD","Srikandi SHD","dianisa","https://assets.dianisa.com/media/2024/03/3.-Era-Trans-Srikandi-SHD.webp"),
 ("sr-primajasa-shd","Primajasa Srikandi SHD","Srikandi SHD","dianisa","https://assets.dianisa.com/media/2024/03/26.-Primajasa-Srikandi-SHD.webp"),
 ("sr-handoyo-shd","Handoyo Srikandi SHD","Srikandi SHD","dianisa","https://assets.dianisa.com/media/2024/03/23.-Handoyo-Srikandi-SHD.webp"),
 ("ct-anak-pantai","Canter Anak Pantai v3","Camion Canter","dianisa","https://assets.dianisa.com/media/2024/07/1.-Anak-Pantai-Livery-Canter-Box-v3.webp"),
 ("ct-armada-sayur","Canter Armada Sayur","Camion Canter","dianisa","https://assets.dianisa.com/media/2024/07/4.-Armada-Sayur.webp"),
 ("ct-merah-meriah","Canter Merah Meriah","Camion Canter","dianisa","https://assets.dianisa.com/media/2024/07/16.-Merah-Meriah.webp"),
 ("tr-pepeje-shd","Tronton Pepeje SHD","Camion Tronton","dianisa","https://assets.dianisa.com/media/2024/07/11.-Pepeje-SHD-Tronton.webp"),
 ("tr-fuso-fn-trailer","Fuso FN Trailer Kontainer","Camion Trailer","Ad iskn","https://assets.dianisa.com/media/2024/07/1.-FUSO-FN-TRAILER-KONTAINER-ad-isknn.webp"),
 ("tr-ud-quester-wingbox","UD Quester Wingbox","Camion Trailer","dianisa","https://assets.dianisa.com/media/2024/07/12.-WINGBOX-UD-QUESTER.webp"),
]

hdr = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
entries, ok, fail = [], 0, 0
for slug, name, veh, author, url in ITEMS:
    try:
        req = urllib.request.Request(url, headers=hdr)
        data = urllib.request.urlopen(req, timeout=60).read()
        img = Image.open(io.BytesIO(data)).convert("RGBA")
        out = os.path.join(PACK, slug + ".png")
        img.save(out, "PNG", optimize=True)
        size = os.path.getsize(out)
        entries.append({
            "id": "lv-" + slug, "name": name, "type": "livery",
            "fileName": slug + ".png", "fileUrl": RAW + slug + ".png",
            "sourcePageUrl": "https://github.com/olivio-bassir/bussid-mod-catalog",
            "previewUrl": RAW + slug + ".png", "author": author,
            "category": veh,
            "description": "Livery " + name + " (" + veh + "), prete a appliquer en un clic.",
            "sizeBytes": size,
        })
        ok += 1
    except Exception as e:
        print("FAIL", slug, "->", e); fail += 1

# Merge dans le catalogue
cat = json.load(open(os.path.join(ROOT,"catalog.json"), encoding="utf-8"))
existing = {m["id"] for m in cat["mods"]}
added = 0
# Inserer les liveries un-clic apres les 3 test liveries + pack couleurs (en tete de section)
for e in entries:
    if e["id"] not in existing:
        cat["mods"].insert(3 + added, e); existing.add(e["id"]); added += 1
cat["version"] = 8
cat["updatedAt"] = "2026-07-10"
json.dump(cat, open(os.path.join(ROOT,"catalog.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"OK={ok} FAIL={fail} ajoutees={added} total_mods={len(cat['mods'])}")
