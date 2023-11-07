famousBirthdays = {'Albert Einstein':'03/14/1879', 'Benjamin Franklin':'01/17/1706', 'Ada Lovelace':'12/10/1815',
                   'Charles Darwin':'02/12/1809', 'Alan Turing':'06/23/1912'}
print('Welcome to the birthday dictionary. We know the burthdays of:')
for listed in famousBirthdays:
    print(listed)
print('Whose birthday do you want to look up?')
name = input()
print(name + '\'s birthday is ' + famousBirthdays[name])