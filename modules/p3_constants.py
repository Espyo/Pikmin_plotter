class Alignment :
    def __init__(self, x, y, r) :
        self.x = x
        self.y = y
        self.r = r

scale = 0.2 # Pikmin 3's radar texture scale.

alignments = {}
alignments["mapb_0"] = Alignment(6, 7, 180)
alignments["mapb_1"] = Alignment(-240, 860, 180)
alignments["mape_3"] = Alignment(-1152, 890, 180)
