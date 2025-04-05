note_length = {
    'full': 1.0,
    'half': 0.5,
    'quarter': 0.25,
    'eighth': 0.125,
    'sixteenth': 0.0625
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

def demons_souls_theme_notes():
    quarter = note_length['quarter']
    half = note_length['half']
    full = note_length['full']

    return (
        # Bar 1
        ("G4", quarter), ("Bb4", quarter), ("D5", half),
        # Bar 2
        ("F4", quarter), ("G4", quarter), ("Bb4", half),
        # Bar 3
        ("D5", quarter), ("C5", quarter), ("Bb4", half),
        # Bar 4
        ("G4", quarter), ("F4", quarter), ("D4", half),
        # Bar 5
        ("G4", quarter), ("Bb4", quarter), ("D5", half),
        # Bar 6
        ("F4", quarter), ("G4", quarter), ("Bb4", half),
        # Bar 7
        ("D5", quarter), ("Eb5", quarter), ("F5", half),
        # Bar 8
        ("G5", quarter), ("F5", quarter), ("Eb5", half),
        # Bar 9
        ("D5", quarter), ("C5", quarter), ("Bb4", half),
        # Bar 10
        ("F4", quarter), ("G4", quarter), ("Bb4", half),
        # Bar 11
        ("D5", quarter), ("Eb5", quarter), ("F5", half),
        # Bar 12
        ("G5", quarter), ("F5", quarter), ("Eb5", half),
        # Bar 13
        ("D5", quarter), ("C5", quarter), ("Bb4", half),
        # Bar 14
        ("F4", quarter), ("G4", quarter), ("Bb4", half),
        # Bar 15
        ("D5", quarter), ("Eb5", quarter), ("F5", half),
        # Bar 16
        ("G5", quarter), ("F5", quarter), ("Eb5", half),
        # Bar 17
        ("D5", half),
        # Bar 18
        ("Eb5", half),
        # Bar 19
        ("F5", half),
        # Bar 20
        ("G5", full)
    )

def demons_souls_theme_bass():
    quarter = note_length['quarter']
    half = note_length['half']
    full = note_length['full']

    return (
        # Bar 1
        ("G2", half), ("G2", half),
        # Bar 2
        ("Bb2", half), ("Bb2", half),
        # Bar 3
        ("D3", half), ("D3", half),
        # Bar 4
        ("F2", half), ("F2", half),
        # Bar 5
        ("G2", half), ("G2", half),
        # Bar 6
        ("Bb2", half), ("Bb2", half),
        # Bar 7
        ("D3", half), ("D3", half),
        # Bar 8
        ("Eb3", half), ("Eb3", half),
        # Bar 9
        ("D3", half), ("D3", half),
        # Bar 10
        ("Bb2", half), ("Bb2", half),
        # Bar 11
        ("D3", half), ("D3", half),
        # Bar 12
        ("Eb3", half), ("Eb3", half),
        # Bar 13
        ("D3", half), ("D3", half),
        # Bar 14
        ("Bb2", half), ("Bb2", half),
        # Bar 15
        ("D3", half), ("D3", half),
        # Bar 16
        ("Eb3", half), ("Eb3", half),
        # Bar 17
        ("D3", half),
        # Bar 18
        ("Eb3", half),
        # Bar 19
        ("F3", half),
        # Bar 20
        ("G3", full),
    )

def majula_theme_melody():
    return (
        # Bar 1
        ("E4", 0.25), ("D4", 0.25), ("C4", 0.5),
        # Bar 2
        ("E4", 0.25), ("G4", 0.25), ("E4", 0.5),
        # Bar 3
        ("F4", 0.25), ("G4", 0.25), ("A4", 0.5),
        # Bar 4
        ("G4", 0.25), ("E4", 0.25), ("C4", 0.5),
        # Bar 5
        ("D4", 0.25), ("E4", 0.25), ("F4", 0.5),
        # Bar 6
        ("G4", 0.25), ("A4", 0.25), ("B4", 0.5),
        # Bar 7
        ("G4", 0.25), ("F4", 0.25), ("E4", 0.5),
        # Bar 8
        ("D4", 0.25), ("E4", 0.25), ("C4", 0.5),

        # Page 2 (Bar 32 onward)
        ("D4", 0.25), ("F4", 0.25), ("A4", 0.5),
        ("B4", 0.25), ("C5", 0.25), ("D5", 0.5),
        ("E5", 0.25), ("D5", 0.25), ("C5", 0.5),
        ("A4", 0.25), ("F4", 0.25), ("D4", 0.5),

        # Bar 40
        ("G4", 0.25), ("E4", 0.25), ("C4", 0.5),
        ("B3", 0.25), ("D4", 0.25), ("G4", 0.5),

        # Final cadence (Bar 96+)
        ("F4", 0.5), ("E4", 0.5),
        ("D4", 1.0), ("C4", 1.0),
        ("C4", 2.0)
    )

def majula_theme_harmony():
    return (
        # Bar 1–8
        ("C3", 0.5), ("E3", 0.5), ("G3", 1.0),
        ("C3", 0.5), ("E3", 0.5), ("G3", 1.0),
        ("D3", 0.5), ("F3", 0.5), ("A3", 1.0),
        ("C3", 0.5), ("E3", 0.5), ("G3", 1.0),
        ("B2", 0.5), ("D3", 0.5), ("F3", 1.0),
        ("C3", 0.5), ("E3", 0.5), ("G3", 1.0),
        ("A2", 0.5), ("C3", 0.5), ("E3", 1.0),
        ("G2", 0.5), ("B2", 0.5), ("D3", 1.0),

        # Bar 32–35
        ("D3", 0.5), ("F3", 0.5), ("A3", 1.0),
        ("B2", 0.5), ("D3", 0.5), ("G3", 1.0),
        ("C3", 0.5), ("E3", 0.5), ("G3", 1.0),
        ("A2", 0.5), ("F3", 0.5), ("D3", 1.0),

        # Bar 40
        ("C3", 0.5), ("G3", 0.5), ("E3", 1.0),
        ("B2", 0.5), ("D3", 0.5), ("G3", 1.0),

        # Final cadence
        ("F3", 1.0), ("E3", 1.0),
        ("D3", 2.0), ("C3", 2.0),
        ("C3", 2.0)
    )

def majula_theme_bass():
    return (
        # Bar 1–8
        ("C2", 2.0), ("C2", 2.0), ("D2", 2.0), ("C2", 2.0),
        ("B1", 2.0), ("C2", 2.0), ("A1", 2.0), ("G1", 2.0),

        # Bar 32–35
        ("D2", 2.0), ("B1", 2.0), ("C2", 2.0), ("A1", 2.0),

        # Bar 40
        ("C2", 2.0), ("G1", 2.0),

        # Final cadence
        ("F2", 2.0), ("E2", 2.0),
        ("D2", 4.0), ("C2", 4.0),
        ("C2", 4.0)
    )
