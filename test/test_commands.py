from commands import Command, ReplyObject, ExternalCommands
from room import Room
from user import User
from app import PSBot
from data.pokedex import Pokedex
import re


psb = PSBot()
test_room = Room('test')
test_user = User('user')

""" Tests the commands that are within the Command method
"""

def testInvalidCommand():
    reply = Command(psb, 'test_command', test_room, '', test_user)
    assert reply == ReplyObject('test_command is not a valid command.'), 'Invalid command not properly recognized; {}'.format(reply.text)


def testAddExternalCommand():
    def test_command(bot, cmd, room, msg, user): return ReplyObject('')
    ExternalCommands.update({'test_command': test_command})
    reply = Command(psb, 'test_command', test_room, '', test_user)
    assert reply.text == ReplyObject('').text, 'External command was not properly recognized'

def testPokemonSmogonAnalysis():
    for p in Pokedex:
        pok = re.sub('-(?:mega(?:-(x|y))?|primal)', '', p, flags=re.I).replace(' ', '').lower()
        substitutes = {'gourgeist-s':'gourgeist-small',
                       'gourgeist-l':'gourgeist-large',
                       'gourgeist-xl':'gourgeist-super',
                       'pumpkaboo-s':'pumpkaboo-small',
                       'pumpkaboo-l':'pumpkaboo-large',
                       'pumpkaboo-xl':'pumpkaboo-super',
                       'giratina-o':'giratina-origin',
                       'mr.mime':'mr_mime',
                       'mimejr.':'mime_jr'}
        pok2 = pok
        if pok in substitutes:
            pok2 = substitutes[pok]
        reply = Command(psb, p.replace(' ', '').lower(), test_room, '', test_user)
        answer = ReplyObject('Analysis: http://www.smogon.com/dex/sm/pokemon/{poke}/'.format(poke=pok2), True)
        assert reply.text == answer.text, '{poke} was not recognized; {rep} == {ans}'.format(poke=pok, rep=reply.text, ans=answer.text)