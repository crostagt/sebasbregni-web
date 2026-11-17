#!/usr/bin/env python3
"""Builds one static, indexable page per category for sebasbregni.com.
Usage: python3 seo_build.py <repo-dir>
Reads content.js (via node) and writes <slug>/index.html, sitemap.xml and robots.txt.
The 3D gallery (index.html) is not modified except the JSON-LD block in <head>."""
import json, os, subprocess, sys, html, datetime

REPO = sys.argv[1]
BASE = "https://sebasbregni.com"
TODAY = datetime.date.today().isoformat()

ROOMS = json.loads(subprocess.check_output(["node", "-e", """
global.window={};require(process.argv[1]);
console.log(JSON.stringify({rooms:window.ROOMS}))""", os.path.join(REPO, "content.js")]))["rooms"]
IMGS = json.loads(subprocess.check_output(["node", "-e", """
global.window={};require(process.argv[1]);console.log(JSON.stringify(window.IMAGES))""",
    os.path.join(REPO, "images/manifest.js")]))

# Category copy (Spanish first: the audience searches from Guatemala)
CAT = {
 "objects": dict(slug="fotografia-de-producto", h1="Fotografía de producto",
   title="Fotografía de producto en Guatemala | Sebas Bregni Photography",
   desc="Fotografía de producto y bodegón en estudio en Guatemala: luz, reflejo, textura y color para marcas, catálogos y redes sociales. Sebas Bregni Photography.",
   intro="Fotografía de producto y bodegón en estudio, en Guatemala. Luz, reflejo, textura y color para marcas, catálogos, e-commerce y redes sociales."),
 "jewelry": dict(slug="fotografia-de-joyeria-y-relojes", h1="Fotografía de joyería y relojes",
   title="Fotografía de joyería y relojes en Guatemala | Sebas Bregni Photography",
   desc="Fotografía de joyería y relojes en Guatemala: macro, detalle y campañas para joyerías y marcas de relojes. Sebas Bregni Photography.",
   intro="Joyería y relojes, de cerca. Macro, detalle y campañas en estudio en Guatemala para joyerías y marcas de relojes."),
 "food": dict(slug="fotografia-de-comida", h1="Fotografía de comida y gastronomía",
   title="Fotografía de comida para restaurantes y hoteles en Guatemala | Sebas Bregni",
   desc="Fotografía gastronómica para restaurantes y hoteles en Guatemala, del huerto a la mesa: platos, bebidas, chefs y ambiente. Sebas Bregni Photography.",
   intro="Fotografía de comida para restaurantes y hoteles en Guatemala, del huerto a la mesa: platos, bebidas, cocineros y ambiente."),
 "motion": dict(slug="fotografia-de-motos", h1="Fotografía de motos y automotriz",
   title="Fotografía de motos y automotriz en Guatemala | Sebas Bregni Photography",
   desc="Fotografía automotriz y de motocicletas en estudio en Guatemala: máquinas iluminadas como escultura. Fotos y video. Sebas Bregni Photography.",
   intro="Fotografía automotriz en estudio en Guatemala. Motocicletas iluminadas como escultura, en foto y video."),
 "people": dict(slug="fotografia-de-moda", h1="Fotografía de moda, belleza y retrato",
   title="Fotografía de moda, belleza y retrato en Guatemala | Sebas Bregni Photography",
   desc="Fotografía de moda, belleza, accesorios y retrato con modelos en estudio en Guatemala, para marcas, catálogos y editoriales. Sebas Bregni Photography.",
   intro="Moda, belleza, accesorios y retrato con modelos en estudio en Guatemala, para marcas, catálogos y editoriales."),
 "animals": dict(slug="fotografia-de-mascotas", h1="Fotografía de mascotas",
   title="Fotografía de mascotas en estudio en Guatemala | Sebas Bregni Photography",
   desc="Fotografía de perros y gatos en estudio en Guatemala: paciencia, luz y expresiones reales. Sesiones de mascotas y marcas pet. Sebas Bregni Photography.",
   intro="Perros y gatos en estudio, en Guatemala. Paciencia, luz y expresiones reales, para familias y marcas de mascotas."),
 "nature": dict(slug="fotografia-de-naturaleza", h1="Fotografía de naturaleza",
   title="Fotografía de naturaleza y macro en Guatemala | Sebas Bregni Photography",
   desc="Fotografía de naturaleza y macro en Guatemala: serpientes, insectos y arañas, de cerca y con su propia luz. Sebas Bregni Photography.",
   intro="Fotografía de naturaleza y macro en Guatemala: serpientes, insectos y arañas, de cerca y con su propia luz."),
 "weddings": dict(slug="fotografia-de-bodas", h1="Fotografía de bodas",
   title="Fotografía de bodas en Guatemala | Sebas Bregni Photography",
   desc="Fotografía de bodas en Guatemala, del vestido al primer baile: preparativos, ceremonia, detalles y fiesta. Sebas Bregni Photography.",
   intro="Fotografía de bodas en Guatemala, del vestido al primer baile: preparativos, ceremonia, detalles y fiesta."),
 "moving-image": dict(slug="video-comercial", h1="Video comercial y reels",
   title="Video comercial y reels para marcas en Guatemala | Sebas Bregni Photography",
   desc="Producción de video comercial y reels para marcas en Guatemala: producto, moda, relojes y motos. Sebas Bregni Photography.",
   intro="Video comercial y reels para marcas en Guatemala: producto, moda, relojes y motos."),
}

# Spanish alt text, written after looking at every photograph
ALT = {
 "cover-products": "Lata de refresco roja sobre hielo picado",
 "coke-red": "Lata de refresco con gotas de agua sobre fondo rojo",
 "g0a3455": "Detalle de la tapa de una lata de refresco con gotas sobre fondo negro",
 "g0a3428": "Lata de refresco roja con reflejo sobre fondo blanco",
 "mg-1864": "Dispositivo negro sobre fondo azul, fotografía de producto",
 "mg-1965": "Dispositivo negro y verde sobre fondo verde, fotografía de producto",
 "mg-1991": "Dispositivo negro y dorado sobre fondo mostaza, fotografía de producto",
 "mg-6168": "Bodegón con florero de vidrio, flores blancas y pedestal de madera sobre fondo beige",
 "mg-6318": "Bodegón con dos floreros blancos y flores lilas sobre fondo beige",
 "cover-jewelry": "Reloj cronógrafo con correa de tela sobre fondo negro",
 "citizen-1": "Cronógrafo Citizen con taquímetro, vista lateral sobre negro",
 "citizen-3": "Detalle de la esfera de un reloj Citizen Eco-Drive",
 "g0a0005": "Esfera de un cronógrafo Citizen Eco-Drive en macro",
 "g0a0187": "Aretes, pulsera y anillo sobre flores de ave del paraíso",
 "g0a0177": "Anillo y dije sobre un tallo de ave del paraíso",
 "g0a3474": "Reloj en su estuche abierto sobre fondo oscuro",
 "0g0a3431": "Anillo en un estuche de madera junto a rosas blancas",
 "mg-1456": "Sándwich con aguacate, queso y cebolla morada en primer plano",
 "mg-1381": "Desayuno servido en una terraza frente al lago de Atitlán y el volcán",
 "mg-1584": "Plato de pollo con verduras y una copa de vino blanco junto a la piscina",
 "mg-0786": "Mesero sosteniendo un plato de ensalada fresca en el jardín",
 "mg-0993": "Salsa de chocolate vertida sobre un pastel de chocolate con fresas",
 "mg-1055": "Crème brûlée con frutos rojos sobre un plato decorado",
 "mg-1788": "Cocinero con una canasta de verduras recién cosechadas en el huerto",
 "mg-1736": "Manos cosechando rábanos en el huerto",
 "mg-5954": "Ceviche con chips y copa de vino blanco en la barra de un restaurante",
 "mg-6033": "Tacos dorados con guacamole y una bebida roja sobre tabla de madera",
 "g0a7916": "Pizza margarita con albahaca y queso rallado, vista cenital",
 "g0a8002": "Pizza con embutido, alcaparras y microbrotes, vista cenital",
 "g0a8036": "Pizza con anchoas, chiles encurtidos y albahaca, vista cenital",
 "g0a7955": "Masa de pizza estirada entre dos manos sobre una mesa enharinada",
 "g0a7942": "Manos enharinadas aplaudiendo sobre un bollo de masa",
 "g0a7854": "Mano doblando masa de pizza sobre una mesa enharinada",
 "mg-1123": "Retrato en blanco y negro de un hombre con lentes y audífonos al cuello",
 "mg-1150": "Retrato de perfil con audífonos en clave baja",
 "mg-1151": "Retrato en tres cuartos con audífonos y lentes en clave baja",
 "mg-1949": "Hombre con sombrero y chaleco exhalando humo en clave baja",
 "mg-1947": "Hombre con sombrero mirando una voluta de humo",
 "mg-9340": "Modelo con top negro y jeans mirando sobre el hombro",
 "mg-9276": "Retrato de belleza con la mano en el hombro sobre fondo gris",
 "mg-9315": "Modelo sentada en un banco vestida de negro sobre fondo gris",
 "mg-8464": "Modelo enmarcada por manos con gorra Hola Guatemala y blusa típica",
 "mg-8574": "Modelo con sombrero verde Hola Guatemala en ángulo selfie",
 "g0a8517": "Retrato de cuerpo entero vestida de negro, mano en la cadera",
 "triumph-34": "Motocicleta Triumph Speed Twin 1200 en tres cuartos sobre fondo negro",
 "triumph-front": "Motocicleta Triumph Speed Twin 1200 de frente, iluminada en estudio",
 "stark-side": "Motocicleta eléctrica Stark Varg de perfil sobre fondo negro",
 "stark-front": "Motocicleta Stark Varg de frente iluminada en estudio",
 "mg-2366": "Detalle del manubrio y el asiento de una Stark Varg",
 "mg-2270": "Detalle de la horquilla y el guardabarros de una Stark Varg",
 "mg-2348": "Detalle del motor eléctrico de una Stark Varg",
 "g0a7515": "Modelo con kimono floral y abanico junto a una puerta de madera",
 "g0a7542": "Kimono, abanico y combinación de encaje sobre fondo rojo",
 "g0a7549": "Modelo con kimono y abanico, una rodilla levantada, sobre fondo rojo",
 "g0a7646": "Modelo con vestido metálico y brazos en alto sobre fondo rosado",
 "g0a7662": "Vestido metálico y viento en el cabello sobre fondo rosado",
 "g0a7655": "Retrato cercano con vestido metálico sobre fondo rosado",
 "g0a3507": "Modelo sosteniendo un frasco de perfume rojo, fotografía de belleza",
 "g0a3507a": "Manos con uñas rojas sosteniendo un frasco de perfume junto a los labios",
 "g0a3513b": "Retrato de belleza de medio rostro con arete dorado en forma de flor",
 "g0a4649": "Modelo recostada con una bolsa de cuero café",
 "g0a4791": "Manos sosteniendo una cartera tejida rosada",
 "g0a5085": "Modelo con blazer negro sosteniendo una cartera roja",
 "g0a4974": "Bolso blanco con monograma de colores en la mano de una modelo",
 "mg-6710": "Modelo con vestido de encaje y lentes de sol sobre fondo rosado",
 "mg-6651": "Retrato de modelo con blusa de encaje sobre fondo rosado",
 "mg-6547": "Modelo con sombrero de paja y chaleco floral sobre fondo beige",
 "mg-6375": "Bolso de rafia al hombro sobre fondo beige",
 "mg-8319": "Retrato en blanco y negro de modelo con la mano en el rostro",
 "mg-8506": "Retrato en blanco y negro de modelo de cabello rizado",
 "mg-8239": "Modelo sentada en el piso, retrato en blanco y negro",
 "cover-models": "Modelo de cuerpo entero con top y leggings negros en estudio blanco",
 "mg-4143": "Modelo sentada con chaqueta camel y pantalón rojo en estudio",
 "g0a8231": "Retrato de modelo de cabello rizado con brazos cruzados en estudio",
 "mg-1022": "Modelo en movimiento lanzando una chaqueta de cuero en estudio",
 "g0a4179-2": "Retrato de un perro pitbull atigrado sobre fondo negro",
 "g0a4282": "Retrato de un perro collie sonriendo sobre fondo negro",
 "g0a4443": "Perro pastor mirando hacia arriba sobre fondo negro",
 "g0a4218": "Perfil de un perro pitbull atigrado sobre fondo negro",
 "g0a8317": "Perro acostado con arnés y correa rosados sobre fondo beige",
 "mg-9230": "Gatito atigrado mirando hacia arriba sobre fondo blanco",
 "mg-9113": "Gatito saltando tras un juguete de plumas sobre fondo blanco",
 "mg-9084": "Gatito atigrado caminando de perfil sobre fondo blanco",
 "mg-9076": "Gatito atigrado sentado mirando a la cámara sobre fondo blanco",
 "img-8774": "Víbora enroscada entre hojas, con luz lateral",
 "img-8813": "Víbora verde sacando la lengua sobre una hoja enroscada",
 "img-8815": "Víbora verde extendida sobre helechos",
 "img-8817": "Víbora verde descansando sobre un helecho",
 "img-8820": "Ojo de una víbora verde en macro",
 "img-8820-v": "Víbora verde, ojo y escamas de cerca",
 "mg-5129": "Culebra bejuquilla extendida sobre fondo negro, de la cola a la cabeza",
 "g0a2055": "Saltamontes hoja sobre una hoja seca, vista de frente",
 "g0a2060": "Saltamontes hoja de perfil sobre una hoja seca",
 "mg-01384": "Cabeza de un insecto palo sobre fondo negro",
 "insecto-palo": "Insecto palo caminando sobre corteza",
 "g0a4261": "Araña tejedora en su telaraña",
 "g0a4289": "Araña tejedora oscura colgando de su hilo",
 "g0a4319": "Patas y rostro de una araña tejedora en macro",
 "0g0a3694": "Novia en bata tocando su vestido colgado de un árbol",
 "0g0a3682": "Vestido de novia colgado de la rama de un árbol",
 "0g0a3548": "Novio y padrinos en el jardín antes de la ceremonia",
 "0g0a5123": "Novios tomados de las manos frente a una ventana de arco",
 "0g0a5155": "Retrato de los novios entre flores en el jardín",
 "0g0a5171": "Novios abrazados frente a una casa de estilo europeo",
 "g0a5341": "Iniciales de los novios y una vela, en blanco y negro",
 "0g0a4989": "Mesa número uno con menú y centro de flores blancas",
 "0g0a5443": "Primer baile de los novios bajo la carpa",
}
FILM_ALT = {
 "film-citizen": "Video del reloj Citizen", "film-triumph": "Video de la Triumph Speed Twin 1200",
 "film-editorial": "Video editorial de moda", "film-environment": "Video de ambiente",
 "film-portrait": "Video de retrato", "film-handbags-1": "Video de carteras",
}

PT = {"Cold light":"Luz fría","Colour study":"Estudio de color","Still life":"Bodegón","Bird of paradise":"Ave del paraíso",
 "Jewelry":"Joyería","Lake Atitlán":"Lago de Atitlán","After dark":"De noche","Silver on pink":"Plata sobre rosa",
 "Beauty":"Belleza","Handbags":"Carteras","Rose":"Rosa","Linen and straw":"Lino y paja","Monochrome":"Blanco y negro",
 "Studio":"Estudio","Snakes":"Serpientes","Insects":"Insectos","Spiders":"Arañas","Dogs":"Perros","Kittens":"Gatitos","Wedding day":"El día de la boda",
 "Wood-fired":"Horno de leña","Low key":"Clave baja","Smoke":"Humo","Black on grey":"Negro sobre gris","Hola, Guatemala":"Hola, Guatemala"}
esc = lambda s: html.escape(s or "", quote=True)

def img_url(i, size=1600):
    m = IMGS[i]; s = size if size in m["sizes"] else m["sizes"][-1]
    return f"/images/{i}-{s}.webp"

def alt_for(w):
    return ALT.get(w.get("img")) or w.get("alt") or ""

CSS = """
:root{--obsidian:#0E0E0E;--ivory:#EDEBE6;--sage:#B5B2AB;--bronze:#C9C4B8;--stone:#94928C;
--serif:"Instrument Serif",Georgia,serif;--sans:"Manrope","Helvetica Neue",Arial,sans-serif}
*{box-sizing:border-box;margin:0}
html,body{background:var(--obsidian);color:var(--ivory)}
body{font-family:var(--sans);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:inherit}
:focus-visible{outline:1px solid var(--bronze);outline-offset:4px}
.wrap{max-width:1280px;margin:0 auto;padding:0 clamp(20px,4vw,48px)}
header{display:flex;justify-content:space-between;align-items:center;padding:28px 0}
.brand{font-family:var(--serif);font-size:22px;letter-spacing:.14em;text-transform:uppercase;text-decoration:none}
.nav{font-weight:500;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--sage)}
.nav a{text-decoration:none;margin-left:22px}
.hero{padding:clamp(48px,10vw,120px) 0 40px;max-width:820px}
h1{font-family:var(--serif);font-weight:400;font-size:clamp(44px,7vw,96px);line-height:.95;letter-spacing:-.01em}
.lead{margin-top:24px;color:var(--sage);font-size:18px;max-width:60ch}
.cta{display:inline-block;margin-top:32px;font-family:var(--serif);font-size:28px;text-decoration:none;border-bottom:1px solid var(--bronze);padding-bottom:3px}
h2{font-family:var(--serif);font-weight:400;font-size:36px;margin:72px 0 24px}
.grid{columns:3 300px;column-gap:16px}
.grid figure{break-inside:avoid;margin:0 0 16px}
.grid img,.grid video{display:block;width:100%;height:auto;background:#1a1a1a}
.grid figcaption{font-size:13px;color:var(--stone);padding:8px 0 4px}
.more{border-top:1px solid #2a2a2a;margin-top:96px;padding:48px 0}
.more h2{margin-top:0;font-size:28px}
.more ul{list-style:none;padding:0;display:flex;flex-wrap:wrap;gap:12px 28px}
.more a{text-decoration:none;color:var(--sage)}
.more a:hover,.nav a:hover{color:var(--ivory)}
footer{padding:32px 0 48px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--stone)}
@media (max-width:640px){.nav a:not(:last-child){display:none}}
"""

def page(r):
    c = CAT[r["id"]]; url = f"{BASE}/{c['slug']}/"
    parts, images = [], []
    for p in r["projects"]:
        if p.get("title"): parts.append(f'<h2>{esc(PT.get(p["title"], p["title"]))}</h2>')
        parts.append('<div class="grid">')
        for w in p["works"]:
            if w.get("film"):
                v = w["video"]; a = FILM_ALT.get(v, "Video")
                parts.append(f'<figure><video controls preload="none" playsinline poster="/videos/{v}-poster.jpg" '
                             f'aria-label="{esc(a)}"><source src="/videos/{v}-720.mp4" type="video/mp4"></video>'
                             f'<figcaption>{esc(a)}</figcaption></figure>')
                continue
            i = w["img"]; m = IMGS[i]; a = alt_for(w)
            h = round(m["h"] * 1600 / m["w"]) if m["w"] > 1600 else m["h"]
            wd = min(m["w"], 1600)
            parts.append(f'<figure><img src="{img_url(i)}" srcset="{img_url(i,800)} 800w, {img_url(i)} 1600w" '
                         f'sizes="(max-width:700px) 100vw, 33vw" width="{wd}" height="{h}" loading="lazy" decoding="async" '
                         f'alt="{esc(a)}"><figcaption>{esc(a)}</figcaption></figure>')
            images.append((img_url(i), a))
        parts.append('</div>')
    others = "".join(f'<li><a href="/{CAT[o["id"]]["slug"]}/">{esc(CAT[o["id"]]["h1"])}</a></li>'
                     for o in ROOMS if o["id"] != r["id"])
    first = images[0][0] if images else "/videos/film-environment-poster.jpg"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url, "url": url, "name": c["title"], "description": c["desc"],
         "inLanguage": "es", "isPartOf": {"@id": BASE + "/#website"}, "about": c["h1"],
         "primaryImageOfPage": BASE + first,
         "hasPart": [{"@type": "ImageObject", "contentUrl": BASE + u, "description": a,
                      "creator": {"@type": "Person", "name": "Sebastián Bregni"},
                      "creditText": "Sebas Bregni Photography",
                      "copyrightNotice": "© Sebas Bregni Photography"} for u, a in images]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Sebas Bregni Photography", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": c["h1"], "item": url}]}]}
    doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
<!-- Google tag -->
<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-WMLQPLCK"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
</script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(c['title'])}</title>
<meta name="description" content="{esc(c['desc'])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(c['title'])}">
<meta property="og:description" content="{esc(c['desc'])}">
<meta property="og:image" content="{BASE + first}">
<meta property="og:locale" content="es_GT">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0E0E0E">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Manrope:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<div class="wrap">
<header><a class="brand" href="/">Sebas Bregni</a>
<nav class="nav" aria-label="Principal"><a href="/#work">Galería</a><a href="/#about">Acerca de</a><a href="/#contact">Cotizar</a></nav></header>
<main>
<section class="hero"><h1>{esc(c['h1'])}</h1><p class="lead">{esc(c['intro'])}</p>
<a class="cta" href="/#{r['id']}">Entrar a la galería 3D</a></section>
{''.join(parts)}
<section class="more"><h2>Otras categorías</h2><ul>{others}</ul>
<p style="margin-top:32px"><a class="cta" href="/#contact">Pedir una cotización</a></p></section>
</main>
<footer>Sebas Bregni Photography · Guatemala · <a href="https://www.instagram.com/sebasbregni_photography/" rel="noopener">Instagram</a></footer>
</div>
</body>
</html>
"""
    d = os.path.join(REPO, c["slug"]); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(doc)
    return url, images

# sitemap with image entries
entries = []
home_imgs = []
for r in ROOMS:
    url, images = page(r)
    home_imgs.append(img_url(r["cover"]["img"]) if r.get("cover", {}).get("img") in IMGS else None)
    entries.append((url, images, "0.8"))
def urlxml(u, imgs, pr):
    im = "".join(f"\n    <image:image><image:loc>{BASE}{esc(i)}</image:loc></image:image>" for i, _ in imgs)
    return f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>{pr}</priority>{im}\n  </url>\n"
sm = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
      'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n')
sm += urlxml(BASE + "/", [(i, "") for i in home_imgs if i], "1.0")
sm += "".join(urlxml(*e) for e in entries) + "</urlset>\n"
open(os.path.join(REPO, "sitemap.xml"), "w").write(sm)
print("pages:", [CAT[r["id"]]["slug"] for r in ROOMS])
print("images in sitemap:", sum(len(e[1]) for e in entries))
missing = [w["img"] for r in ROOMS for p in r["projects"] for w in p["works"] if w.get("img") and not alt_for(w)]
print("missing alt:", missing)
