from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect


CUSTOMERS = []
LINE_OF_CARS = {'change_oil': [],
                'inflate_tires': [],
                'diagnostic': []}
NEXT_TICKET = None


def estimate_time(service):
    if service == 'change_oil':
        mins = len(LINE_OF_CARS['change_oil']) * 2
    elif service == 'inflate_tires':
        mins = len(LINE_OF_CARS['change_oil']) * 2 + len(LINE_OF_CARS['inflate_tires']) * 5
    else:
        mins = len(LINE_OF_CARS['change_oil']) * 2 \
               + len(LINE_OF_CARS['inflate_tires']) * 5 \
               + len(LINE_OF_CARS['diagnostic']) * 30
    return mins


def get_next_ticket():
    if LINE_OF_CARS['change_oil']:
        return LINE_OF_CARS['change_oil'].pop(0)
    if LINE_OF_CARS['inflate_tires']:
        return LINE_OF_CARS['inflate_tires'].pop(0)
    if LINE_OF_CARS['diagnostic']:
        return LINE_OF_CARS['diagnostic'].pop(0)
    return None


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    template_name = 'menu.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class TicketView(View):
    template_name = 'ticket.html'

    def get(self, request, link, *args, **kwargs):
        mins = estimate_time(service=link)
        CUSTOMERS.append(request.user)
        num_ticket = len(CUSTOMERS)
        LINE_OF_CARS[link].append(num_ticket)

        context = {'num_ticket': num_ticket, 'mins': mins}
        return render (request, self.template_name, context=context)


class NextCustomerView(View):
    def get(self, request, *args, **kwargs):
        global NEXT_TICKET
        if NEXT_TICKET:
            message = f'Next ticket #{NEXT_TICKET}'
        else:
            message = 'Waiting for the next client'

        return render(request, 'next.html', context={'message': message})


class ProcessingView(View):
    template_name = 'processing.html'

    def get(self, request, *args, **kwargs):
        context = {
            'oil_q': len(LINE_OF_CARS['change_oil']),
            'tires_q': len(LINE_OF_CARS['inflate_tires']),
            'diagnostic_q': len(LINE_OF_CARS['diagnostic'])
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        global NEXT_TICKET
        NEXT_TICKET = get_next_ticket()
        return redirect('/next')

