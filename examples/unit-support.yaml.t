var1 : 1
var2 : some string
var3 : 3
var4 : $(${var3} + math.pi + 2)
var5 : $(${var4} + 2.0)
var8 : 2 cm
var9 : 4 cm
var10 : 5 mm
var11 : $( (${var9|>q} - ${var8|>q}) / ${var10|>q} |> to "" |> float)
