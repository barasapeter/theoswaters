from datetime import date, datetime
from typing import Type

def classmethods(cls):
    '''Decorate all methods with @classmethod in a class.'''
    for name, value in vars(cls).items():
        # Check if the attribute is a function
        if callable(value):
            # Check if a method is not already a class method
            if not getattr(value, '__call__'):
                # Decorate the function with @classmethod
                setattr(cls, name, classmethod(value))
    return cls

@classmethods
class CustomCalendar:
    return_type: Type[str]

    def date_today():
        '''Returns date in YYYY-MM-DD'''
        return date.today().strftime('%Y-%m-%d')
    
    def time_now():
        '''Returns time in H:M:S'''
        return datetime.now().strftime('%H:%M:%S')
    
    def week_day_name(date_YYYY_MM_DD: str):
        '''Be sure to supply date in YYYY-MM-DD. Returns a day name of the week.'''
        return datetime.strptime(date_YYYY_MM_DD, '%Y-%m-%d').strftime('%A')
    
    def day_name_today():
        '''Returns today's day name'''
        return CustomCalendar.week_day_name(CustomCalendar.date_today())
    

if __name__ == '__main__':
    print(CustomCalendar.time_now())
