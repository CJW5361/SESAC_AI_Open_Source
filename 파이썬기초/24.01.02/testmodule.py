import mod1
# import pathtest.mod2 as mod2
import sys
print('-'*50)
print(sys.path)
print('-'*50)
##############################################################################
sys.path.append(r'C:\Users\USER\Desktop\SESAC\24.01.02\pathtest')
sys.path.append(r'C:\Users\USER\Desktop\SESAC\24.01.02\game')
print('-'*50)
print(sys.path)
print('-'*50)

###########################################################################
import mod2
print(mod1.add(3,4))
print(mod1.sub(4,2))

result=mod2.add(3,4)
print(result)

###########################################################################

# import game.sound.echo
# game.sound.echo.echo_test()
import game.graphic.render
game.graphic.render.render_test()


from game.sound.echo import echo_test
echo_test()


