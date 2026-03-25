import os
import glob
import json

themes = {
    "sanosat": {
        "title": "SanoSat-II",
        "folder": "sanosat_gallery",
        "primary": "#10b981",
        "secondary": "#34d399",
        "bg_accent": "rgba(16, 185, 129, 0.08)",
        "glow": "rgba(16, 185, 129, 0.3)",
        "category": "PocketQube Satellite · Earth Observation",
        "description": "SanoSat-II is a PocketQube satellite scheduled for orbital deployment, focused on Earth observation and imaging. Gagan contributed to satellite imaging mission design, hardware design (multi-layer PCBs), antenna design, subsystem testing, link budget analysis, and technical documentation.",
        "theme_style": "mission-control"
    },
    "decimalsat": {
        "title": "Decimal Sat",
        "folder": "decimalsat_gallery",
        "primary": "#f59e0b",
        "secondary": "#fbbf24",
        "bg_accent": "rgba(245, 158, 11, 0.08)",
        "glow": "rgba(245, 158, 11, 0.3)",
        "category": "PocketQube Satellite · Bio-Product Carrier",
        "description": "Decimal Sat is a PocketQube satellite designed for Earth observation, imaging, and bio-product carrying. Gagan contributed to communication systems, power management, firmware development, PCB design, antenna design, board-level integration, testing, and technical reporting.",
        "theme_style": "bio-lab"
    },
    "vegafly": {
        "title": "VegaFly",
        "folder": "vegafly_gallery",
        "primary": "#06b6d4",
        "secondary": "#22d3ee",
        "bg_accent": "rgba(6, 182, 212, 0.08)",
        "glow": "rgba(6, 182, 212, 0.3)",
        "category": "Remote Sensing Satellite · Imaging",
        "description": "VegaFly is a satellite project aimed at imaging and remote sensing applications. Gagan was engaged in firmware development, power subsystem design, radio communication, hardware design (PCBs), functional testing, and documentation.",
        "theme_style": "aerospace"
    }
}

theme_css = {
    "mission-control": """
        /* === MISSION CONTROL === */
        #gallery-sanosat .gallery-container {
            background-color: #060a0f;
            background-image:
                linear-gradient(rgba(16, 185, 129, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(16, 185, 129, 0.03) 1px, transparent 1px);
            background-size: 40px 40px;
        }
        #gallery-sanosat .project-hero h1 { font-family: 'Outfit', monospace; letter-spacing: 3px; text-transform: uppercase; font-size: 2.5rem; }
        #gallery-sanosat .project-category { font-family: 'Courier New', monospace; letter-spacing: 4px; font-size: 0.75rem; }
        #gallery-sanosat .project-desc { border-left: 3px solid var(--theme-primary); padding-left: 1.2rem; }
        #gallery-sanosat .carousel-slide img { border-radius: 4px; border: 1px solid rgba(16, 185, 129, 0.3); box-shadow: 0 0 20px rgba(16, 185, 129, 0.15); }
    """,
    "bio-lab": """
        /* === BIO-LAB === */
        #gallery-decimalsat .gallery-container {
            background: #0c0a08;
            background-image:
                radial-gradient(ellipse at 20% 50%, rgba(245, 158, 11, 0.04) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 50%, rgba(251, 191, 36, 0.03) 0%, transparent 50%);
        }
        #gallery-decimalsat .project-hero::before { width: 600px; height: 600px; background: radial-gradient(ellipse, rgba(245, 158, 11, 0.15) 0%, rgba(251, 191, 36, 0.05) 40%, transparent 70%); filter: blur(100px); }
        #gallery-decimalsat .project-hero h1 { font-size: 3.2rem; }
        #gallery-decimalsat .project-desc { background: rgba(245, 158, 11, 0.04); padding: 1.2rem 1.5rem; border-radius: 20px; border: 1px solid rgba(245, 158, 11, 0.1); }
        #gallery-decimalsat .carousel-slide img { border-radius: 24px; box-shadow: 0 10px 40px rgba(245, 158, 11, 0.2); }
    """,
    "aerospace": """
        /* === AEROSPACE === */
        #gallery-vegafly .gallery-container {
            background: #050a10;
            background-image:
                linear-gradient(135deg, rgba(6, 182, 212, 0.02) 25%, transparent 25%),
                linear-gradient(225deg, rgba(6, 182, 212, 0.02) 25%, transparent 25%),
                linear-gradient(45deg, rgba(6, 182, 212, 0.02) 25%, transparent 25%),
                linear-gradient(315deg, rgba(6, 182, 212, 0.02) 25%, transparent 25%);
            background-size: 60px 60px; background-position: 0 0, 0 30px, 30px -30px, -30px 0px;
        }
        #gallery-vegafly .project-hero::before { width: 500px; height: 200px; background: linear-gradient(90deg, transparent, rgba(6, 182, 212, 0.15), transparent); filter: blur(60px); top: 0; }
        #gallery-vegafly .project-hero h1 { letter-spacing: 5px; text-transform: uppercase; font-weight: 900; }
        #gallery-vegafly .project-category { letter-spacing: 5px; border: 1px solid rgba(6, 182, 212, 0.25); display: inline-block; padding: 0.4rem 1.2rem; }
        #gallery-vegafly .carousel-slide img { border-radius: 0; border: 1px solid rgba(6, 182, 212, 0.4); }
        #gallery-vegafly .carousel-nav, #gallery-vegafly .lightbox-nav { clip-path: polygon(15% 0, 100% 0, 85% 100%, 0% 100%); border-radius: 0; width: 60px; }
    """
}

# Core 3D Carousel and Lightbox CSS (Global for all overlays)
gallery_core_css = """
.carousel-wrapper {
    position: relative;
    width: 100%;
    height: 500px;
    margin: 40px 0;
    perspective: 1500px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: visible;
}

.carousel-slide {
    position: absolute;
    width: 60%;
    max-width: 800px;
    aspect-ratio: 16/9;
    transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    transform-style: preserve-3d;
    cursor: pointer;
    overflow: hidden;
}

.carousel-slide img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
}

.carousel-slide:hover img {
    transform: scale(1.05);
}

.carousel-nav {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(0,0,0,0.5);
    color: white;
    border: 1px solid rgba(255,255,255,0.2);
    width: 50px;
    height: 50px;
    border-radius: 50%;
    font-size: 1.5rem;
    cursor: pointer;
    z-index: 1000;
    transition: all 0.3s ease;
    backdrop-filter: blur(5px);
}

.carousel-nav:hover {
    background: var(--theme-primary);
    border-color: transparent;
    box-shadow: 0 0 20px var(--theme-glow);
}

.carousel-prev { left: 5%; }
.carousel-next { right: 5%; }

.carousel-status {
    text-align: center;
    font-family: 'Outfit', sans-serif;
    font-size: 1.1rem;
    margin-bottom: 40px;
    opacity: 0.7;
}

.gallery-bottom {
    margin-top: auto;
    padding: 2rem;
    text-align: left;
}

.back-btn {
    background: transparent;
    border: 1px solid rgba(255,255,255,0.2);
    color: white;
    padding: 0.8rem 1.5rem;
    border-radius: 30px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.back-btn:hover {
    background: rgba(255,255,255,0.1);
    border-color: white;
}

/* Lightbox Styling */
.lightbox {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.95);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 10000;
    opacity: 0;
    visibility: hidden;
    transition: all 0.4s ease;
    backdrop-filter: blur(15px);
}

.lightbox.active {
    opacity: 1;
    visibility: visible;
}

.lightbox-img-wrapper {
    position: relative;
    max-width: 90%;
    max-height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.lightbox-img {
    max-width: 100%;
    max-height: 80vh;
    object-fit: contain;
    border: 2px solid rgba(255,255,255,0.1);
    box-shadow: 0 0 50px rgba(255,255,255,0.1);
    transition: opacity 0.3s ease;
}

.lightbox-close {
    position: absolute;
    top: 2rem;
    right: 2rem;
    background: none;
    border: none;
    color: white;
    font-size: 3rem;
    cursor: pointer;
    line-height: 1;
    opacity: 0.6;
    transition: opacity 0.3s;
}

.lightbox-close:hover { opacity: 1; }

.lightbox-nav {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(255,255,255,0.05);
    color: white;
    border: 1px solid rgba(255,255,255,0.1);
    width: 60px;
    height: 60px;
    border-radius: 50%;
    font-size: 2rem;
    cursor: pointer;
    z-index: 100;
    transition: all 0.3s ease;
}

.lightbox-nav:hover { background: rgba(255,255,255,0.2); transform: translateY(-50%) scale(1.1); }
.lightbox-prev { left: -80px; }
.lightbox-next { right: -80px; }

.lightbox-counter {
    margin-top: 2rem;
    color: white;
    font-family: 'Outfit', sans-serif;
    letter-spacing: 2px;
    opacity: 0.6;
}

@media (max-width: 768px) {
    .lightbox-nav { width: 45px; height: 45px; font-size: 1.5rem; }
    .lightbox-prev { left: 1rem; }
    .lightbox-next { right: 1rem; }
    .carousel-slide { width: 85%; }
}
"""

# The template container for each individual gallery overlay
gallery_template = """
<div id="gallery-{pid}" class="gallery-overlay">
    <button onclick="closeGallery()" class="close-overlay-btn" title="Close Gallery">&times;</button>
    <div class="gallery-container" style="--theme-primary: {primary}; --theme-glow: {glow};">
        
        <div class="project-hero">
            <h1>{title} <span>Gallery</span></h1>
            <p class="project-category">{category}</p>
            <p class="project-desc">{description}</p>
        </div>

        <div class="carousel-wrapper" id="{pid}-carousel-wrapper">
            {carousel_html}
            <button class="carousel-nav carousel-prev" id="{pid}-prev">&#8249;</button>
            <button class="carousel-nav carousel-next" id="{pid}-next">&#8250;</button>
        </div>
        
        <div class="carousel-status"><span id="{pid}-current">1</span> / <span>{carousel_count}</span></div>

        <div class="gallery-bottom">
            <button onclick="closeGallery()" class="back-btn">Go Back to Portfolio</button>
        </div>
        
    </div>
</div>
"""

# Store image paths in a global window object for the lightbox
js_images_block = "<script>\nwindow.GALLERY_DATA = {\n"

combined_html = ""
all_css = ""

for pid, cfg in themes.items():
    images = []
    for ext in ["*.jpeg", "*.png", "*.jpg"]:
        images.extend(glob.glob(f"images/{cfg['folder']}/{ext}"))

    images = [img.replace("\\\\", "/").replace("\\", "/") for img in sorted(images)]
    js_images_block += f"    '{pid}': {json.dumps(images)},\n"

    carousel_html = ""
    for i, img in enumerate(images):
         carousel_html += f'<div class="carousel-slide {pid}-slide" data-index="{i}"><img src="{img}" alt="{cfg["title"]} photo {i+1}"></div>\n            '

    combined_html += gallery_template.format(
        pid=pid,
        title=cfg["title"],
        primary=cfg["primary"],
        glow=cfg["glow"],
        category=cfg["category"],
        description=cfg["description"],
        carousel_html=carousel_html,
        carousel_count=len(images)
    )
    
    all_css += theme_css.get(cfg["theme_style"], "")

all_css = gallery_core_css + all_css

js_images_block += "};\n</script>\n"

# Lightbox template that works across all galleries
lightbox_html = """
<div class="lightbox" id="spa-lightbox">
    <button class="lightbox-close" id="spa-lb-close">&times;</button>
    <div class="lightbox-img-wrapper">
        <button class="lightbox-nav lightbox-prev" id="spa-lb-prev">&#8249;</button>
        <img class="lightbox-img" id="spa-lb-img" src="" alt="Gallery Full Image">
        <button class="lightbox-nav lightbox-next" id="spa-lb-next">&#8250;</button>
    </div>
    <div class="lightbox-counter"><span id="spa-lb-current">1</span> / <span id="spa-lb-total">1</span></div>
</div>
"""

# Update style.css directly via script (faster than manual injection later)
STYLE_CSS_PATH = 'style.css'
with open(STYLE_CSS_PATH, 'r', encoding='utf-8') as f:
    style_content = f.read()

# Append gallery specific CSS if not already there
MARKER = "/* === DYNAMIC GALLERY CSS === */"
if MARKER in style_content:
    style_content = style_content[:style_content.find(MARKER)]

with open(STYLE_CSS_PATH, 'w', encoding='utf-8') as f:
    f.write(style_content + "\n" + MARKER + "\n" + all_css)

# Generate the snippet file
with open("galleries_snippet.html", "w", encoding="utf-8") as f:
    f.write(combined_html + lightbox_html + js_images_block)

print("Generated galleries_snippet.html and updated style.css.")
