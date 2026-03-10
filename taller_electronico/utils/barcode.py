from xml.sax.saxutils import escape

CODE39_MAP = {
    "0": "101001101101", "1": "110100101011", "2": "101100101011", "3": "110110010101",
    "4": "101001101011", "5": "110100110101", "6": "101100110101", "7": "101001011011",
    "8": "110100101101", "9": "101100101101", "A": "110101001011", "B": "101101001011",
    "C": "110110100101", "D": "101011001011", "E": "110101100101", "F": "101101100101",
    "G": "101010011011", "H": "110101001101", "I": "101101001101", "J": "101011001101",
    "K": "110101010011", "L": "101101010011", "M": "110110101001", "N": "101011010011",
    "O": "110101101001", "P": "101101101001", "Q": "101010110011", "R": "110101011001",
    "S": "101101011001", "T": "101011011001", "U": "110010101011", "V": "100110101011",
    "W": "110011010101", "X": "100101101011", "Y": "110010110101", "Z": "100110110101",
    "-": "100101011011", ".": "110010101101", " ": "100110101101", "$": "100100100101",
    "/": "100100101001", "+": "100101001001", "%": "101001001001", "*": "100101101101",
}


def code39_svg(value: str, height: int = 80, bar_width: int = 2) -> str:
    clean = (value or "").upper().strip()
    if not clean:
        clean = "VACIO"
    clean = ''.join(ch for ch in clean if ch in CODE39_MAP and ch != '*')
    encoded = f"*{clean}*"

    bits = []
    for idx, ch in enumerate(encoded):
        pattern = CODE39_MAP[ch]
        bits.append(pattern)
        if idx < len(encoded) - 1:
            bits.append("0")
    bitstream = ''.join(bits)

    width = len(bitstream) * bar_width + 20
    x = 10
    rects = []
    for bit in bitstream:
        if bit == "1":
            rects.append(f'<rect x="{x}" y="8" width="{bar_width}" height="{height}" fill="#111827" />')
        x += bar_width

    text = escape(clean)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height + 28}" '
        f'viewBox="0 0 {width} {height + 28}">' 
        f'<rect width="100%" height="100%" fill="#fff"/>{"".join(rects)}'
        f'<text x="{width / 2}" y="{height + 20}" font-size="14" text-anchor="middle" fill="#111827" '
        f'font-family="Arial, sans-serif">{text}</text></svg>'
    )
