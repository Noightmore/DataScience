note_length = {
    'full': 1.0,
    'half': 0.5,
    'quarter': 0.25,
    'eighth': 0.125,
    'sixteenth': 0.0625,
    'double': 2.0,
    'quadruple': 4.0
}



def dark_souls_theme_notes():
    eighth = note_length['eighth']
    return (
        # Bar 1
        ("E4", eighth), ("G4", eighth), ("A4", eighth), ("B4", eighth),
        ("A4", eighth), ("G4", eighth), ("E4", eighth), ("G4", eighth),
        # Bar 2
        ("F4", eighth), ("A4", eighth), ("B4", eighth), ("C5", eighth),
        ("B4", eighth), ("A4", eighth), ("F4", eighth), ("A4", eighth),
        # Bar 3
        ("E4", eighth), ("G4", eighth), ("A4", eighth), ("B4", eighth),
        ("A4", eighth), ("G4", eighth), ("E4", eighth), ("G4", eighth),
        # Bar 4
        ("F4", eighth), ("A4", eighth), ("B4", eighth), ("C5", eighth),
        ("B4", eighth), ("A4", eighth), ("F4", eighth), ("A4", eighth),
        # Bar 5
        ("E4", eighth), ("G4", eighth), ("A4", eighth), ("B4", eighth),
        ("A4", eighth), ("G4", eighth), ("E4", eighth), ("G4", eighth),
        # Bar 6
        ("F4", eighth), ("A4", eighth), ("B4", eighth), ("C5", eighth),
        ("B4", eighth), ("A4", eighth), ("F4", eighth), ("A4", eighth),
        # Bar 7
        ("E4", eighth), ("G4", eighth), ("A4", eighth), ("B4", eighth),
        ("A4", eighth), ("G4", eighth), ("E4", eighth), ("G4", eighth),
        # Bar 8
        ("F4", eighth), ("A4", eighth), ("B4", eighth), ("C5", eighth),
        ("B4", eighth), ("A4", eighth), ("F4", eighth), ("A4", eighth),
    )


def dark_souls_theme_bass():
    full = note_length['full']
    return (
        # Bar 1
        ("E2", full),
        # Bar 2
        ("E2", full),
        # Bar 3
        ("E2", full),
        # Bar 4
        ("E2", full),
        # Bar 5
        ("E2", full),
        # Bar 6
        ("E2", full),
        # Bar 7
        ("rest", full),  # <- REST
        # Bar 8
        ("E2", full),
    )



def demons_souls_theme_notes():
    quarter = note_length['quarter']
    full = note_length['full']

    return (
        # Bar 1–2
        ("G4", quarter), ("Bb4", quarter), ("D5", quarter), ("F5", quarter + full),  # Bar 1 + 2

        # Bar 3–4
        ("F4", quarter), ("G4", quarter), ("Bb4", quarter), ("D5", quarter + full),  # Bar 3 + 4

        # Bar 5–6
        ("D5", quarter), ("C5", quarter), ("Bb4", quarter), ("F4", quarter + full),  # Bar 5 + 6

        # Bar 7–8
        ("G4", quarter), ("F4", quarter), ("D4", quarter), ("C4", quarter + full),   # Bar 7 + 8

        # Bar 9–10
        ("G4", quarter), ("Bb4", quarter), ("D5", quarter), ("F5", quarter + full),  # Bar 9

        # Bar 11–12
        ("F4", quarter), ("G4", quarter), ("Bb4", quarter), ("D5", quarter + full),  # Bar 11

        # Bar 13–14
        ("D5", quarter), ("Eb5", quarter), ("F5", quarter), ("G5", quarter + full),  # Bar 13 + 14

        # Bar 15–16
        ("G5", quarter), ("F5", quarter), ("Eb5", quarter), ("D5", quarter + full),  # Bar 15 + 16

        # Bar 17–18
        ("D5", quarter), ("C5", quarter), ("Bb4", quarter), ("F4", quarter + full),  # Bar 17 + 18

        # Bar 19–20
        ("F4", quarter), ("G4", quarter), ("Bb4", quarter), ("D5", quarter + full),  # Bar 19 + 20
    )



def demons_souls_theme_bass():
    half = note_length['half']
    full = note_length['full']
    double = note_length['double']

    return (
        # Bar 1
        ("G2", full),
        # Bar 2
        ("Bb2", full),
        # Bar 3
        ("D3", full),
        # Bar 4
        ("F2", full),
        # Bar 5
        ("G2", full),
        # Bar 6
        ("Bb2", full),
        # Bar 7
        ("D3", full),
        # Bar 8
        ("Eb3", full),
        # Bar 9
        ("D3", full),
        # Bar 10
        ("Bb2", full),
        # Bar 11
        ("D3", full),
        # Bar 12
        ("Eb3", full),
        # Bar 13
        ("D3", full),
        # Bar 14
        ("Bb2", full),
        # Bar 15
        ("D3", full),
        # Bar 16
        ("Eb3", full),
        # Bar 17
        ("D3", full),
        # Bar 18
        ("Eb3", full),
        # Bar 19
        ("F3", full),
        # Bar 20
        ("G3", full)
    )


def majula_theme_melody():
    quarter = note_length['quarter']
    half = note_length['half']
    full = note_length['full']
    double = note_length['double']

    return (
        # Bar 1
        ("E4", quarter), ("D4", quarter), ("C4", half),
        # Bar 2
        ("E4", quarter), ("G4", quarter), ("E4", half),
        # Bar 3
        ("F4", quarter), ("G4", quarter), ("A4", half),
        # Bar 4
        ("G4", quarter), ("E4", quarter), ("C4", half),
        # Bar 5
        ("D4", quarter), ("E4", quarter), ("F4", half),
        # Bar 6
        ("G4", quarter), ("A4", quarter), ("B4", half),
        # Bar 7
        ("G4", quarter), ("F4", quarter), ("E4", half),
        # Bar 8
        ("D4", quarter), ("E4", quarter), ("C4", half),

        # Page 2 (Bar 32 onward)
        ("D4", quarter), ("F4", quarter), ("A4", half),
        ("B4", quarter), ("C5", quarter), ("D5", half),
        ("E5", quarter), ("D5", quarter), ("C5", half),
        ("A4", quarter), ("F4", quarter), ("D4", half),

        # Bar 40
        ("G4", quarter), ("E4", quarter), ("C4", half),
        ("B3", quarter), ("D4", quarter), ("G4", half),

        # Final cadence (Bar 96+)
        ("F4", half), ("E4", half),
        ("D4", full), ("C4", full),
        ("C4", double)
    )



def majula_theme_harmony():
    half = note_length['half']
    full = note_length['full']
    double = note_length['double']
    quadruple = note_length['quadruple']

    return (
        # Bar 1–8
        ("C3", half), ("E3", half), ("G3", full),
        ("C3", half), ("E3", half), ("G3", full),
        ("D3", half), ("F3", half), ("A3", full),
        ("C3", half), ("E3", half), ("G3", full),
        ("B2", half), ("D3", half), ("F3", full),
        ("C3", half), ("E3", half), ("G3", full),
        ("A2", half), ("C3", half), ("E3", full),
        ("G2", half), ("B2", half), ("D3", full),

        # Bar 32–35 (rest in 36–39)
        ("D3", half), ("F3", half), ("A3", full),
        ("B2", half), ("D3", half), ("G3", full),
        ("C3", half), ("E3", half), ("G3", full),
        ("A2", half), ("F3", half), ("D3", full),

        # Bar 36–39: RESTS
        ("REST", double), ("REST", double),

        # Bar 40
        ("C3", half), ("G3", half), ("E3", full),
        ("B2", half), ("D3", half), ("G3", full),

        # Bar 42–48: RESTS
        ("REST", double), ("REST", double), ("REST", double), ("REST", double),
        ("REST", double), ("REST", double), ("REST", double),

        # Final cadence (Bar 49+)
        ("F3", full), ("E3", full),
        ("D3", double), ("C3", double),
        ("C3", double)
    )



def majula_theme_bass():
    double = note_length['double']
    quadruple = note_length['quadruple']

    return (
        # Bar 1–8
        ("C2", double), ("C2", double), ("D2", double), ("C2", double),
        ("B1", double), ("C2", double), ("A1", double), ("G1", double),

        # Bar 32–35
        ("D2", double), ("B1", double), ("C2", double), ("A1", double),

        # Bar 36–39: RESTS
        ("REST", double), ("REST", double),

        # Bar 40
        ("C2", double), ("G1", double),

        # Bar 42–48: RESTS
        ("REST", double), ("REST", double), ("REST", double), ("REST", double),
        ("REST", double), ("REST", double), ("REST", double),

        # Final cadence
        ("F2", double), ("E2", double),
        ("D2", quadruple), ("C2", quadruple),
        ("C2", quadruple)
    )




