var1 : 1
var2 : some string
var3 : 3
var4 : $(${var3} + math.pi + 2)
var5 : $(${var4} + 2.0)
nest1 : &nest
  var1 : 11
  var2 : $(${var3} + 12)
  var3 : $(${var1} + 12)
  var4 : $(${var3} + 12)
  var5 : $(${/nest1/var3} + 12)
  nest2 :
    var1 : 111
    var2 : 112
    var3 : $(${var1})
    var4 : $(${/var1})
    var5 : $(${/nest1/var1})
