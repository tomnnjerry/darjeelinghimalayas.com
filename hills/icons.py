"""Line icons (24×24, stroke = currentColor). One per land, one per experience kind, plus UI icons.

Drawn for this site; render with {% icon "darjeeling" %} or {% icon "darjeeling" "icon--lg" %}.
"""

ICONS = {
    # ---- lands
    "darjeeling":  # B-class toy-train steam engine on the two-foot line
        '<path d="M2 19.6h20"/><path d="M4 15.9V10h9v5.9"/><path d="M13 15.9V7h5v8.9"/><path d="M12.4 7h6.2"/>'
        '<path d="M6 10V7.6h2V10"/><path d="M7 5.6c0-1.1 1-1.6 2-1.6s1.6-1 2.6-1"/><path d="M14.8 9h1.8v2h-1.8z"/>'
        '<path d="M3 13.5h1"/><circle cx="6.5" cy="17.6" r="1.6"/><circle cx="11" cy="17.6" r="1.6"/><circle cx="16" cy="17.6" r="1.6"/>',
    "kurseong-mirik":  # a cup of first flush with a fresh leaf
        '<path d="M4 11h12v3a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M16 12h1.5a2 2 0 0 1 0 4H16"/><path d="M3 21h14"/>'
        '<path d="M9 9c-1.5-2-1-4.5 2-6 1 2.5.5 4.5-2 6z"/><path d="M9 9c.6-1.5 1.2-2.8 2-4"/>',
    "kalimpong":  # orchid flower on its stem
        '<circle cx="12" cy="11" r="1.2"/><path d="M12 9.8C10.6 7.5 10.8 5 12 3.5c1.2 1.5 1.4 4 0 6.3z"/>'
        '<path d="M10.8 10.6C8.5 9.8 6 10.3 4.5 11.8c2 1.3 4.5 1.2 6.3-.2z"/><path d="M13.2 10.6c2.3-.8 4.8-.3 6.3 1.2-2 1.3-4.5 1.2-6.3-.2z"/>'
        '<path d="M12 12.3c-1.8 1.2-2.4 3.2-1.5 4.8 1 .3 2 .3 3 0 .9-1.6.3-3.6-1.5-4.8z"/><path d="M12 17.5V21M12 19.5c1.5-1 3-1 4-.5"/>',
    "singalila":  # the ridge, a summit flag and the trail
        '<path d="M2 19l5-7 3 3 4-7 8 11z"/><path d="M14 8V3.5l3 1.2-3 1.3"/><path d="M5 21.5c3-1 5-.5 7-2s3-3 4-3" stroke-dasharray="1 2"/>',
    "gangtok":  # prayer flags strung over a high lake
        '<path d="M3 21V5M21 21V5"/><path d="M3 6c5 3 13 3 18 0"/><path d="M6 7.4v3h2.2V8M10.5 8.5v3h2.2V8.7M15 8.3v3h2.2V7.8"/>'
        '<path d="M5 18c2-1 4-1 7 0s5 1 7 0"/>',
    "north-sikkim":  # glacier peak above a sacred lake
        '<path d="M2 17l6.5-10 3 4.5 2.5-3L22 17z"/><path d="M6.6 10l1.9 1.4 1.3-1.2 1.7 1.3"/><path d="M5 20.5c2.5-1 5-1 7 0s4.5 1 7 0"/>',
    "west-sikkim":  # chorten: steps, dome, harmika and spire
        '<path d="M4 21h16M6 21v-2.5h12V21M7.5 18.5V16h9v2.5"/><path d="M8 16c0-2.5 1.8-4 4-4s4 1.5 4 4"/>'
        '<path d="M10.8 12v-1.5h2.4V12"/><path d="M11.2 10.5L12 4.5l.8 6"/><path d="M11.4 8h1.2M11.6 6.3h.8"/><path d="M12 4.5V3"/>',
    "dooars":  # one-horned rhino
        '<path d="M3 16c0-3 2.5-5.5 6-5.5h5c2 0 3.5 1 4.5 2.5l2 1-1 2.5h-2l-.5 3h-2v-2.5H10V19H8v-2.5c-2.5 0-5-.5-5-.5z"/>'
        '<path d="M20.5 14l1.3-3"/><path d="M16 10.6l.5-2 1.2 1.6"/><path d="M17.8 13.2h.01"/>',
    # ---- experience kinds
    "viewpoint": '<path d="M3 19l6-9 3.5 5 2.5-3.5L21 19z"/><circle cx="17" cy="6" r="2"/><path d="M17 2.3v.9M20.7 6h-.9M14.4 3.4l.6.6M19.6 3.4l-.6.6"/>',
    "monastery": '<path d="M3 21h18"/><path d="M5 21v-7h14v7"/><path d="M3.5 14l2-3h13l2 3"/><path d="M7 11V8.5h10V11"/>'
                 '<path d="M6 8.5l1.5-2h9l1.5 2"/><path d="M12 6.5V3.5"/><path d="M10.5 21v-3.5h3V21"/>',
    "culture": '<path d="M3 21h18"/><path d="M4.5 21v-9L12 6l7.5 6v9"/><path d="M16 8.8V5h2v5.4"/><path d="M10 21v-4.5h4V21"/>'
               '<path d="M7 13.5h2v2H7zM15 13.5h2v2h-2z"/>',
    "tea": '<path d="M12 21c-.5-5.5 1.5-10 7-13.5.5 6.5-2 11-7 13.5z"/><path d="M12 21c-4-1.5-7-5-7-10.5 4 1.5 6.5 4.5 7 10.5z"/>'
           '<path d="M12 21c.3-3 1.5-6 4-8.5M12 21c-1-2.5-2.5-5-5-7"/><path d="M12.5 7c-.8-1.6-.6-3 .5-4 1 1.2.9 2.6-.5 4z"/>',
    "rail": '<rect x="6" y="3.5" width="12" height="13" rx="3"/><path d="M6 10h12"/><path d="M9 6.5h6"/><circle cx="9" cy="13.3" r="1"/>'
            '<circle cx="15" cy="13.3" r="1"/><path d="M8 16.5L5.5 21M16 16.5l2.5 4.5M7 19.3h10"/>',
    "trek": '<circle cx="12.5" cy="4.5" r="1.8"/><path d="M12 7.5L10 13l3 3 1 5M10 13l-2 8"/><path d="M12.2 8.5l3.2 2.5 2-.5"/>'
            '<path d="M17.5 9v12"/><path d="M11.5 8l-3 1.5-1 3"/>',
    "wildlife": '<circle cx="6" cy="10" r="1.8"/><circle cx="10" cy="6" r="1.8"/><circle cx="14" cy="6" r="1.8"/><circle cx="18" cy="10" r="1.8"/>'
                '<path d="M8 17c0-3 1.8-5 4-5s4 2 4 5c0 2-1.8 3-4 3s-4-1-4-3z"/>',
    "food": '<path d="M4 15c0-4 3.5-7 8-7s8 3 8 7z"/><path d="M8.5 9.4c.6 1.5 1 3.2.8 5.6M12 8v7M15.5 9.4c-.6 1.5-1 3.2-.8 5.6"/>'
            '<path d="M3 15h18l-1.5 4h-15z"/><path d="M10 5.5c0-1 .8-1.3.8-2.3M13.5 5.5c0-1 .8-1.3.8-2.3"/>',
    "craft": '<path d="M4 3v18M20 3v18M3 5h18M3 19h18"/><path d="M7.5 5v14M10.5 5v14M13.5 5v14M16.5 5v14" stroke-dasharray="2 1.6"/>',
    "adventure": '<path d="M3 15h18l-2 3.5H5z"/><path d="M8 15l6-11M13.2 5.5l1.6.9"/><path d="M2 21.5c2-.8 4-.8 6 0s4 .8 6 0 4-.8 6 0"/>',
    # ---- UI
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "book": '<path d="M4 4h6a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4z"/><path d="M20 4h-6a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h7z"/>',
    "route": '<circle cx="6" cy="18" r="2"/><circle cx="18" cy="6" r="2"/><path d="M8 18h6a3 3 0 0 0 0-6h-4a3 3 0 0 1 0-6h6"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 10h8M8 13h5"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "sparkle": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
    "ticket": '<path d="M3 7h18v3a2 2 0 0 0 0 4v3H3v-3a2 2 0 0 0 0-4z"/><path d="M14.5 7v10" stroke-dasharray="1.5 2"/>',
    "rupee": '<path d="M6 4h12M6 8.5h12M6 4h3.5a4.5 4.5 0 0 1 0 9H6l8 7"/>',
    "jeep": '<path d="M3 15v-4l2-4h9l2 4h3a2 2 0 0 1 2 2v2z"/><circle cx="7" cy="16.5" r="2"/><circle cx="17" cy="16.5" r="2"/><path d="M6 11h9M10 7v4"/>',
    "home": '<path d="M3 11l9-7 9 7"/><path d="M5 10v11h14V10"/><path d="M10 21v-6h4v6"/>',
    "altitude": '<path d="M2 20l7-12 4 6 2-3 7 9z"/><path d="M18 3v7M16 5l2-2 2 2"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "bed": '<path d="M3 18V6M3 14h18v4M21 14v-2a3 3 0 0 0-3-3h-7v5"/><circle cx="7" cy="11" r="1.8"/>',
    "pin": '<path d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "mist": '<path d="M3 9h12M6 13h15M3 17h12"/>',
    "flag": '<path d="M5 21V4M5 4h11l-2 3.5L16 11H5"/>',
    "story": '<path d="M5 4h11l3 3v13H5z"/><path d="M8 9h8M8 12.5h8M8 16h5"/>',
    "leaf": '<path d="M5 19c0-8 5-14 15-15 0 10-6 15-14 15z"/><path d="M5 19c3-4 6-7 10-10"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "whatsapp": '<path d="M20 12a8 8 0 0 1-11.8 7L4 20l1.1-4A8 8 0 1 1 20 12z"/><path d="M9 9.5c.3 2.2 2.3 4.2 4.5 4.5l1.2-1.2-1.8-1-.8.6a3.4 3.4 0 0 1-1.6-1.6l.6-.8-1-1.8z"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "arrow-up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
}


def svg(name, cls=""):
    body = ICONS.get(name) or ICONS["sparkle"]
    return (f'<svg class="icon {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')
