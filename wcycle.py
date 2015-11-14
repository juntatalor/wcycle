"""
Women cycle calculator

"""

from models import Woman
import datetime


def get_cycle(date1, date2, cycle):
    days = (date2 - date1).days
    period = days % cycle
    if 0 <= period <= 4:
        return 'Periods right now'
    elif 5 <= period <= 11:
        return '1-st period (right after)'
    elif 12 <= period <= 19:
        return '2-nd period (much time after)'
    else:
        return '3-d period (right before)'


def women_list():
    q = Woman.select()
    if q.count():
        for woman in q:
            print('%s. Name: %s' % (woman.id, woman.full_name))
    else:
        print('No women info yet. Press key to return')
        input('')
        main_menu()

    print('Choose one of the following:')
    print('1. Detail')
    print('2. New')
    print('3. Return to main menu')

    val = input('Choice:')
    if val == '1':
        woman_detail()
    elif val == '2':
        new_woman()
    else:
        main_menu()


def woman_detail():
    woman_id = input('Woman id:')

    try:
        woman = Woman.get(Woman.id == woman_id)
        print('Full name: %s' % woman.full_name)
        print('Stability: %s' % woman.wc_stability)
        print('Cycle: %s' % woman.wc_cycle)
        print('Last cycle: %s' % woman.wc_last_cycle)
        print('Current phase: %s' % get_cycle(woman.wc_last_cycle, datetime.date.today(), woman.wc_cycle))
        print('')
        print('Choose one of the following:')
        print('1. Edit')
        print('2. Delete')
        print('3. Return to list')
        val = input('Choice:')
        if val == '1':
            woman_edit(woman)
        elif val == '2':
            woman_delete(woman)
        elif val == '3':
            women_list()
        else:
            main_menu()

    except Woman.DoesNotExist:
        print('No woman with such id')
        main_menu()


def new_woman():
    full_name = input('Full name:')
    if not full_name:
        print('You should enter proper name')
        new_woman()
    s_wc_stability = input('Stability 0: stable, 1: unstable (default - stable):')
    if s_wc_stability not in ['0', '1']:
        wc_stability = 0
    else:
        wc_stability = int(s_wc_stability)
    s_wc_cycle = input('Cycle, days (default - 28):')
    try:
        wc_cycle = int(s_wc_cycle)
    except ValueError:
        wc_cycle = 28
    s_wc_last_cycle = input('Last cycle yy-mm-dd (default: today)')
    try:
        wc_last_cycle = datetime.datetime.strptime(s_wc_last_cycle, '%y-%m-%d')
    except ValueError:
        wc_last_cycle = datetime.date.today()

    Woman.create(full_name=full_name, wc_stability=wc_stability, wc_cycle=wc_cycle, wc_last_cycle=wc_last_cycle)
    print('Woman info created! Press key to return.')
    input()
    main_menu()


def woman_edit(woman):
    full_name = input('Full name (default - %s):' % woman.full_name)
    if not full_name:
        full_name = woman.full_name
    s_wc_stability = input('Stability 0: stable, 1: unstable (default - %s):' % woman.wc_stability)
    if s_wc_stability not in ['0', '1']:
        wc_stability = woman.wc_stability
    else:
        wc_stability = int(s_wc_stability)
    s_wc_cycle = input('Cycle, days  (default - %s):' % woman.wc_cycle)
    try:
        wc_cycle = int(s_wc_cycle)
    except ValueError:
        wc_cycle = woman.wc_cycle
    s_wc_last_cycle = input('Last cycle yy-mm-dd (default: %s)' % woman.wc_cycle)
    try:
        wc_last_cycle = datetime.datetime.strptime(s_wc_last_cycle, '%y-%m-%d')
        if wc_last_cycle > datetime.date.today():
            print('Last cycle from future. Set to today.')
            wc_last_cycle = datetime.date.today()
    except ValueError:
        print('Last cycle set to today')
        wc_last_cycle = woman.wc_cycle

    woman.full_name=full_name
    woman.wc_stability=wc_stability
    woman.wc_cycle=wc_cycle
    woman.wc_last_cycle=wc_last_cycle
    woman.save()
    print('Woman info updated! Press key to return.')
    input()
    main_menu()


def woman_delete(woman):
    woman.delete_instance()
    print('Delete succesfull! Press key to retun.')
    input()
    main_menu()


def main_menu():
    print('Welcome to women cycle calculator beta version')
    print('Choose one of the following:')
    print('1. Women list')
    print('2. Store new woman data')
    print('3. Exit')

    val = input('Choice:')
    if val == '1':
        women_list()
    elif val == '2':
        new_woman()
    elif val == '3':
        exit()
    else:
        print('Wrong input')
        main_menu()


if __name__ == '__main__':
    main_menu()
