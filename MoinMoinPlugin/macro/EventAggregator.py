# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - EventAggregator Macro

    @copyright: 2008, 2009, 2010 by Paul Boddie <paul@boddie.org.uk>
    @copyright: 2000-2004 Juergen Hermann <jh@web.de>,
                2005-2008 MoinMoin:ThomasWaldmann.
    @license: GNU GPL (v2 or later), see COPYING.txt for details.
"""

from MoinMoin import wikiutil
import EventAggregatorSupport
import calendar

linkToPage = EventAggregatorSupport.linkToPage

Dependencies = ['pages']

# Abstractions.

class View:

    "A view of the event calendar."

    def __init__(self, page, calendar_name, raw_calendar_start, raw_calendar_end,
        original_calendar_start, original_calendar_end, calendar_start, calendar_end,
        first, last, category_names, template_name, parent_name, mode, name_usage):

        """
        Initialise the view with the current 'page', a 'calendar_name' (which
        may be None), the 'raw_calendar_start' and 'raw_calendar_end' (which
        are the actual start and end values provided by the request), the
        calculated 'original_calendar_start' and 'original_calendar_end' (which
        are the result of calculating the calendar's limits from the raw start
        and end values), and the requested, calculated 'calendar_start' and
        'calendar_end' (which may involve different start and end values due to
        navigation in the user interface), along with the 'first' and 'last'
        months of event coverage.

        The additional 'category_names', 'template_name', 'parent_name' and
        'mode' parameters are used to configure the links employed by the view.

        The 'name_usage' parameter controls how names are shown on calendar mode
        events.
        """

        self.page = page
        self.calendar_name = calendar_name
        self.raw_calendar_start = raw_calendar_start
        self.raw_calendar_end = raw_calendar_end
        self.original_calendar_start = original_calendar_start
        self.original_calendar_end = original_calendar_end
        self.calendar_start = calendar_start
        self.calendar_end = calendar_end
        self.template_name = template_name
        self.parent_name = parent_name
        self.mode = mode
        self.name_usage = name_usage

        self.category_name_parameters = "&".join([("category=%s" % name) for name in category_names])

        if self.calendar_name is not None:

            # Store the view parameters.

            self.number_of_months = (last - first).months() + 1

            self.previous_month_start = first.previous_month()
            self.next_month_start = first.next_month()
            self.previous_month_end = last.previous_month()
            self.next_month_end = last.next_month()

            self.previous_set_start = first.month_update(-self.number_of_months)
            self.next_set_start = first.month_update(self.number_of_months)
            self.previous_set_end = last.month_update(-self.number_of_months)
            self.next_set_end = last.month_update(self.number_of_months)

    def getQualifiedParameterName(self, argname):

        "Return the 'argname' qualified using the calendar name."

        return EventAggregatorSupport.getQualifiedParameterName(self.calendar_name, argname)

    def getMonthYearQueryString(self, argname, year_month, prefix=1):

        """
        Return a query string fragment for the given 'argname', referring to the
        month given by the specified 'year_month' object, appropriate for this
        calendar.

        If 'prefix' is specified and set to a false value, the parameters in the
        query string will not be calendar-specific, but could be used with the
        summary action.
        """

        if year_month is not None:
            year, month = year_month.as_tuple()
            month_argname = "%s-month" % argname
            year_argname = "%s-year" % argname
            if prefix:
                month_argname = self.getQualifiedParameterName(month_argname)
                year_argname = self.getQualifiedParameterName(year_argname)
            return "%s=%s&%s=%s" % (month_argname, month, year_argname, year)
        else:
            return ""

    def getMonthQueryString(self, argname, month, prefix=1):

        """
        Return a query string fragment for the given 'argname', referring to the
        month given by the specified 'month' value, appropriate for this
        calendar.

        If 'prefix' is specified and set to a false value, the parameters in the
        query string will not be calendar-specific, but could be used with the
        summary action.
        """

        if month is not None:
            if prefix:
                argname = self.getQualifiedParameterName(argname)
            return "%s=%s" % (argname, month)
        else:
            return ""

    def getNavigationLink(self, start, end, mode=None):

        """
        Return a query string fragment for navigation to a view showing months
        from 'start' to 'end' inclusive, with the optional 'mode' indicating the
        view style.
        """

        return "%s&%s&%s=%s" % (
            self.getMonthQueryString("start", start),
            self.getMonthQueryString("end", end),
            self.getQualifiedParameterName("mode"), mode or self.mode
            )

    def getFullMonthLabel(self, year_month):
        page = self.page
        request = page.request
        return EventAggregatorSupport.getFullMonthLabel(request, year_month)

    def writeDownloadControls(self):
        page = self.page
        request = page.request
        fmt = page.formatter
        _ = request.getText

        output = []

        # Generate the links.

        download_dialogue_link = "action=EventAggregatorSummary&parent=%s&%s" % (
            self.parent_name or "",
            self.category_name_parameters
            )
        download_all_link = download_dialogue_link + "&doit=1"
        download_link = download_all_link + ("&%s&%s" % (
            self.getMonthYearQueryString("start", self.calendar_start, prefix=0),
            self.getMonthYearQueryString("end", self.calendar_end, prefix=0)
            ))

        # Subscription links just explicitly select the RSS format.

        subscribe_dialogue_link = download_dialogue_link + "&format=RSS"
        subscribe_all_link = download_all_link + "&format=RSS"
        subscribe_link = download_link + "&format=RSS"

        # Adjust the "download all" and "subscribe all" links if the calendar
        # has an inherent period associated with it.

        period_limits = []

        if self.raw_calendar_start:
            period_limits.append("&%s" %
                self.getMonthQueryString("start", self.raw_calendar_start, prefix=0)
                )
        if self.raw_calendar_end:
            period_limits.append("&%s" %
                self.getMonthQueryString("end", self.raw_calendar_end, prefix=0)
                )

        period_limits = "".join(period_limits)

        download_dialogue_link += period_limits
        download_all_link += period_limits
        subscribe_dialogue_link += period_limits
        subscribe_all_link += period_limits

        # Pop-up descriptions of the downloadable calendars.

        calendar_period = (self.calendar_start or self.calendar_end) and \
            "%s - %s" % (
                self.getFullMonthLabel(self.calendar_start),
                self.getFullMonthLabel(self.calendar_end)
                ) or _("All events")

        original_calendar_period = (self.original_calendar_start or self.original_calendar_end) and \
            "%s - %s" % (
                self.getFullMonthLabel(self.original_calendar_start),
                self.getFullMonthLabel(self.original_calendar_end)
                ) or _("All events")

        raw_calendar_period = (self.raw_calendar_start or self.raw_calendar_end) and \
            "%s - %s" % (self.raw_calendar_start, self.raw_calendar_end) or _("No period specified")

        # Write the controls.

        # Download controls.

        output.append(fmt.div(on=1, css_class="event-download-controls"))
        output.append(fmt.span(on=1, css_class="event-download"))
        output.append(linkToPage(request, page, _("Download this view"), download_link))
        output.append(fmt.span(on=1, css_class="event-download-popup"))
        output.append(fmt.text(calendar_period))
        output.append(fmt.span(on=0))
        output.append(fmt.span(on=0))

        output.append(fmt.span(on=1, css_class="event-download"))
        output.append(linkToPage(request, page, _("Download this calendar"), download_all_link))
        output.append(fmt.span(on=1, css_class="event-download-popup"))
        output.append(fmt.span(on=1, css_class="event-download-period"))
        output.append(fmt.text(original_calendar_period))
        output.append(fmt.span(on=0))
        output.append(fmt.span(on=1, css_class="event-download-period-raw"))
        output.append(fmt.text(raw_calendar_period))
        output.append(fmt.span(on=0))
        output.append(fmt.span(on=0))
        output.append(fmt.span(on=0))

        output.append(fmt.span(on=1, css_class="event-download"))
        output.append(linkToPage(request, page, _("Download..."), download_dialogue_link))
        output.append(fmt.span(on=1, css_class="event-download-popup"))
        output.append(fmt.text(_("Edit download options")))
        output.append(fmt.span(on=0))
        output.append(fmt.span(on=0))

        # Subscription controls.

        output.append(fmt.span(on=1, css_class="event-download"))
        output.append(linkToPage(request, page, _("Subscribe to this view"), subscribe_link))
        output.append(fmt.span(on=1, css_class="event-download-popup"))
        output.append(fmt.text(calendar_period))
        output.append(fmt.span(on=0))
        output.append(fmt.span(on=0))

        output.append(fmt.span(on=1, css_class="event-download"))
        output.append(linkToPage(request, page, _("Subscribe to this calendar"), subscribe_all_link))
        output.append(fmt.span(on=1, css_class="event-download-popup"))
        output.append(fmt.span(on=1, css_class="event-download-period"))
        output.append(fmt.text(original_calendar_period))
        output.append(fmt.span(on=0))
        output.append(fmt.span(on=1, css_class="event-download-period-raw"))
        output.append(fmt.text(raw_calendar_period))
        output.append(fmt.span(on=0))
        output.append(fmt.span(on=0))
        output.append(fmt.span(on=0))

        output.append(fmt.span(on=1, css_class="event-download"))
        output.append(linkToPage(request, page, _("Subscribe..."), subscribe_dialogue_link))
        output.append(fmt.span(on=1, css_class="event-download-popup"))
        output.append(fmt.text(_("Edit subscription options")))
        output.append(fmt.span(on=0))
        output.append(fmt.span(on=0))
        output.append(fmt.div(on=0))

        return "".join(output)

    def writeViewControls(self):
        page = self.page
        request = page.request
        fmt = page.formatter
        _ = request.getText

        output = []

        calendar_link = self.getNavigationLink(
            self.calendar_start, self.calendar_end, "calendar"
            )
        list_link = self.getNavigationLink(
            self.calendar_start, self.calendar_end, "list"
            )
        table_link = self.getNavigationLink(
            self.calendar_start, self.calendar_end, "table"
            )

        # Write the controls.

        output.append(fmt.div(on=1, css_class="event-view-controls"))
        output.append(fmt.span(on=1, css_class="event-view"))
        output.append(linkToPage(request, page, _("View as calendar"), calendar_link))
        output.append(fmt.span(on=0))
        output.append(fmt.span(on=1, css_class="event-view"))
        output.append(linkToPage(request, page, _("View as list"), list_link))
        output.append(fmt.span(on=0))
        output.append(fmt.span(on=1, css_class="event-view"))
        output.append(linkToPage(request, page, _("View as table"), table_link))
        output.append(fmt.span(on=0))
        output.append(fmt.div(on=0))

        return "".join(output)

    def writeMonthHeading(self, year_month):
        page = self.page
        request = page.request
        fmt = page.formatter
        _ = request.getText
        full_month_label = self.getFullMonthLabel(year_month)

        output = []

        # Prepare navigation links.

        if self.calendar_name is not None:
            calendar_name = self.calendar_name

            # Links to the previous set of months and to a calendar shifted
            # back one month.

            previous_set_link = self.getNavigationLink(
                self.previous_set_start, self.previous_set_end
                )
            previous_month_link = self.getNavigationLink(
                self.previous_month_start, self.previous_month_end
                )

            # Links to the next set of months and to a calendar shifted
            # forward one month.

            next_set_link = self.getNavigationLink(
                self.next_set_start, self.next_set_end
                )
            next_month_link = self.getNavigationLink(
                self.next_month_start, self.next_month_end
                )

            # A link leading to this month being at the top of the calendar.

            end_month = year_month.month_update(self.number_of_months - 1)

            month_link = self.getNavigationLink(year_month, end_month)

            output.append(fmt.span(on=1, css_class="previous-month"))
            output.append(linkToPage(request, page, "<<", previous_set_link))
            output.append(fmt.text(" "))
            output.append(linkToPage(request, page, "<", previous_month_link))
            output.append(fmt.span(on=0))

            output.append(fmt.span(on=1, css_class="next-month"))
            output.append(linkToPage(request, page, ">", next_month_link))
            output.append(fmt.text(" "))
            output.append(linkToPage(request, page, ">>", next_set_link))
            output.append(fmt.span(on=0))

            output.append(linkToPage(request, page, full_month_label, month_link))

        else:
            output.append(fmt.span(on=1))
            output.append(fmt.text(full_month_label))
            output.append(fmt.span(on=0))

        return "".join(output)

    def writeDayNumberLinked(self, date):
        page = self.page
        request = page.request
        fmt = page.formatter
        _ = request.getText

        year, month, day = date.as_tuple()
        output = []

        # Prepare navigation details for the calendar shown with the new event
        # form.

        navigation_link = self.getNavigationLink(
            self.calendar_start, self.calendar_end, self.mode
            )

        # Prepare the link to the new event form, incorporating the above
        # calendar parameters.

        new_event_link = "action=EventAggregatorNewEvent&start-day=%d&start-month=%d&start-year=%d" \
            "&%s&template=%s&parent=%s&%s" % (
            day, month, year, self.category_name_parameters, self.template_name, self.parent_name or "",
            navigation_link)

        output.append(fmt.div(on=1))
        output.append(fmt.span(on=1, css_class="event-day-number"))
        output.append(linkToPage(request, page, unicode(day), new_event_link))
        output.append(fmt.span(on=0))
        output.append(fmt.div(on=0))

        return "".join(output)

    # Calendar layout methods.

    def writeDayNumbers(self, first_day, number_of_days, month, busy_dates):
        page = self.page
        fmt = page.formatter

        output = []
        output.append(fmt.table_row(on=1))

        for weekday in range(0, 7):
            day = first_day + weekday
            date = month.as_date(day)

            # Output out-of-month days.

            if day < 1 or day > number_of_days:
                output.append(fmt.table_cell(on=1,
                    attrs={"class" : "event-day-heading event-day-excluded", "colspan" : "3"}))
                output.append(fmt.table_cell(on=0))

            # Output normal days.

            else:
                if date in busy_dates:
                    output.append(fmt.table_cell(on=1,
                        attrs={"class" : "event-day-heading event-day-busy", "colspan" : "3"}))
                else:
                    output.append(fmt.table_cell(on=1,
                        attrs={"class" : "event-day-heading event-day-empty", "colspan" : "3"}))

                # Output the day number, making a link to a new event
                # action.

                output.append(self.writeDayNumberLinked(date))

                # End of day.

                output.append(fmt.table_cell(on=0))

        # End of day numbers.

        output.append(fmt.table_row(on=0))
        return "".join(output)

    def writeEmptyWeek(self, first_day, number_of_days):
        page = self.page
        fmt = page.formatter

        output = []
        output.append(fmt.table_row(on=1))

        for weekday in range(0, 7):
            day = first_day + weekday

            # Output out-of-month days.

            if day < 1 or day > number_of_days:
                output.append(fmt.table_cell(on=1,
                    attrs={"class" : "event-day-content event-day-excluded", "colspan" : "3"}))
                output.append(fmt.table_cell(on=0))

            # Output empty days.

            else:
                output.append(fmt.table_cell(on=1,
                    attrs={"class" : "event-day-content event-day-empty", "colspan" : "3"}))

        output.append(fmt.table_row(on=0))
        return "".join(output)

    def writeWeekSlots(self, first_day, number_of_days, month, week_end, week_slots):
        output = []

        locations = week_slots.keys()
        locations.sort(EventAggregatorSupport.sort_none_first)

        # Visit each slot corresponding to a location (or no location).

        for location in locations:

            # Visit each coverage span, presenting the events in the span.

            for coverage, events in week_slots[location]:

                # Output each set.

                output.append(self.writeWeekSlot(first_day, number_of_days, month, week_end, coverage, events))

                # Add a spacer.

                output.append(self.writeSpacer(first_day, number_of_days))

        return "".join(output)

    def writeWeekSlot(self, first_day, number_of_days, month, week_end, coverage, events):
        page = self.page
        request = page.request
        fmt = page.formatter

        output = []
        output.append(fmt.table_row(on=1))

        # Then, output day details.

        for weekday in range(0, 7):
            day = first_day + weekday
            date = month.as_date(day)

            # Skip out-of-month days.

            if day < 1 or day > number_of_days:
                output.append(fmt.table_cell(on=1,
                    attrs={"class" : "event-day-content event-day-excluded", "colspan" : "3"}))
                output.append(fmt.table_cell(on=0))
                continue

            # Output the day.

            if date not in coverage:
                output.append(fmt.table_cell(on=1,
                    attrs={"class" : "event-day-content event-day-empty", "colspan" : "3"}))

            # Get event details for the current day.

            for event in events:
                event_page = event.getPage()
                event_details = event.getDetails()

                if not (event_details["start"] <= date <= event_details["end"]):
                    continue

                # Get basic properties of the event.

                starts_today = event_details["start"] == date
                ends_today = event_details["end"] == date
                event_summary = event.getSummary(self.parent_name)
                is_ambiguous = event_details["start"].ambiguous() or event_details["end"].ambiguous()

                # Generate a colour for the event.

                bg = getColour(event_summary)
                fg = getBlackOrWhite(bg)
                style = ("background-color: rgb(%d, %d, %d); color: rgb(%d, %d, %d);" % (bg + fg))

                # Determine if the event name should be shown.

                start_of_period = starts_today or weekday == 0 or day == 1

                if self.name_usage == "daily" or start_of_period:
                    hide_text = 0
                else:
                    hide_text = 1

                # Output start of day gap and determine whether
                # any event content should be explicitly output
                # for this day.

                if starts_today:

                    # Single day events...

                    if ends_today:
                        colspan = 3
                        event_day_type = "event-day-single"

                    # Events starting today...

                    else:
                        output.append(fmt.table_cell(on=1, attrs={"class" : "event-day-start-gap"}))
                        output.append(fmt.table_cell(on=0))

                        # Calculate the span of this cell.
                        # Events whose names appear on every day...

                        if self.name_usage == "daily":
                            colspan = 2
                            event_day_type = "event-day-starting"

                        # Events whose names appear once per week...

                        else:
                            if event_details["end"] <= week_end:
                                event_length = event_details["end"].day() - day + 1
                                colspan = (event_length - 2) * 3 + 4
                            else:
                                event_length = week_end.day() - day + 1
                                colspan = (event_length - 1) * 3 + 2

                            event_day_type = "event-day-multiple"

                # Events continuing from a previous week...

                elif start_of_period:

                    # End of continuing event...

                    if ends_today:
                        colspan = 2
                        event_day_type = "event-day-ending"

                    # Events continuing for at least one more day...

                    else:

                        # Calculate the span of this cell.
                        # Events whose names appear on every day...

                        if self.name_usage == "daily":
                            colspan = 3
                            event_day_type = "event-day-full"

                        # Events whose names appear once per week...

                        else:
                            if event_details["end"] <= week_end:
                                event_length = event_details["end"].day() - day + 1
                                colspan = (event_length - 1) * 3 + 2
                            else:
                                event_length = week_end.day() - day + 1
                                colspan = event_length * 3

                            event_day_type = "event-day-multiple"

                # Continuing events whose names appear on every day...

                elif self.name_usage == "daily":
                    if ends_today:
                        colspan = 2
                        event_day_type = "event-day-ending"
                    else:
                        colspan = 3
                        event_day_type = "event-day-full"

                # Continuing events whose names appear once per week...

                else:
                    colspan = None

                # Output the main content only if it is not
                # continuing from a previous day.

                if colspan is not None:

                    # Colour the cell for continuing events.

                    attrs={
                        "class" : "event-day-content event-day-busy %s" % event_day_type,
                        "colspan" : str(colspan)
                        }

                    if not (starts_today and ends_today):
                        attrs["style"] = style

                    output.append(fmt.table_cell(on=1, attrs=attrs))

                    # Output the event.

                    if starts_today and ends_today or not hide_text:

                        # The event box contains the summary, alongside
                        # other elements.

                        output.append(fmt.div(on=1, css_class="event-summary-box"))
                        output.append(fmt.div(on=1, css_class="event-summary", style=style))

                        if is_ambiguous:
                            output.append(fmt.icon("/!\\"))

                        output.append(event_page.linkToPage(request, event_summary))
                        output.append(fmt.div(on=0))

                        # Add a pop-up element for long summaries.

                        output.append(fmt.div(on=1, css_class="event-summary-popup", style=style))

                        if is_ambiguous:
                            output.append(fmt.icon("/!\\"))

                        output.append(event_page.linkToPage(request, event_summary))
                        output.append(fmt.div(on=0))

                        output.append(fmt.div(on=0))

                    # Output end of day content.

                    output.append(fmt.div(on=0))

                # Output end of day gap.

                if ends_today and not starts_today:
                    output.append(fmt.table_cell(on=1, attrs={"class" : "event-day-end-gap"}))
                    output.append(fmt.table_cell(on=0))

            # End of day.

            output.append(fmt.table_cell(on=0))

        # End of set.

        output.append(fmt.table_row(on=0))
        return "".join(output)

    def writeSpacer(self, first_day, number_of_days):
        page = self.page
        fmt = page.formatter

        output = []
        output.append(fmt.table_row(on=1))

        for weekday in range(0, 7):
            day = first_day + weekday
            css_classes = "event-day-spacer"

            # Skip out-of-month days.

            if day < 1 or day > number_of_days:
                css_classes += " event-day-excluded"

            output.append(fmt.table_cell(on=1, attrs={"class" : css_classes, "colspan" : "3"}))
            output.append(fmt.table_cell(on=0))

        output.append(fmt.table_row(on=0))
        return "".join(output)

# HTML-related functions.

def getColour(s):
    colour = [0, 0, 0]
    digit = 0
    for c in s:
        colour[digit] += ord(c)
        colour[digit] = colour[digit] % 256
        digit += 1
        digit = digit % 3
    return tuple(colour)

def getBlackOrWhite(colour):
    if sum(colour) / 3.0 > 127:
        return (0, 0, 0)
    else:
        return (255, 255, 255)

# Macro functions.

def execute(macro, args):

    """
    Execute the 'macro' with the given 'args': an optional list of selected
    category names (categories whose pages are to be shown), together with
    optional named arguments of the following forms:

      start=YYYY-MM     shows event details starting from the specified month
      start=current-N   shows event details relative to the current month
      end=YYYY-MM       shows event details ending at the specified month
      end=current+N     shows event details relative to the current month

      mode=calendar     shows a calendar view of events
      mode=list         shows a list of events by month
      mode=table        shows a table of events

      names=daily       shows the name of an event on every day of that event
      names=weekly      shows the name of an event once per week

      calendar=NAME     uses the given NAME to provide request parameters which
                        can be used to control the calendar view

      template=PAGE     uses the given PAGE as the default template for new
                        events (or the default template from the configuration
                        if not specified)

      parent=PAGE       uses the given PAGE as the parent of any new event page
    """

    request = macro.request
    fmt = macro.formatter
    page = fmt.page
    _ = request.getText

    # Interpret the arguments.

    try:
        parsed_args = args and wikiutil.parse_quoted_separated(args, name_value=False) or []
    except AttributeError:
        parsed_args = args.split(",")

    parsed_args = [arg for arg in parsed_args if arg]

    # Get special arguments.

    category_names = []
    raw_calendar_start = None
    raw_calendar_end = None
    calendar_start = None
    calendar_end = None
    mode = None
    name_usage = "weekly"
    calendar_name = None
    template_name = getattr(request.cfg, "event_aggregator_new_event_template", "EventTemplate")
    parent_name = None

    for arg in parsed_args:
        if arg.startswith("start="):
            raw_calendar_start = arg[6:]

        elif arg.startswith("end="):
            raw_calendar_end = arg[4:]

        elif arg.startswith("mode="):
            mode = arg[5:]

        elif arg.startswith("names="):
            name_usage = arg[6:]

        elif arg.startswith("calendar="):
            calendar_name = arg[9:]

        elif arg.startswith("template="):
            template_name = arg[9:]

        elif arg.startswith("parent="):
            parent_name = arg[7:]

        else:
            category_names.append(arg)

    original_calendar_start = calendar_start = EventAggregatorSupport.getParameterMonth(raw_calendar_start)
    original_calendar_end = calendar_end = EventAggregatorSupport.getParameterMonth(raw_calendar_end)

    # Find request parameters to override settings.

    calendar_start = EventAggregatorSupport.getFormMonth(request, calendar_name, "start") or calendar_start
    calendar_end = EventAggregatorSupport.getFormMonth(request, calendar_name, "end") or calendar_end

    mode = EventAggregatorSupport.getQualifiedParameter(request, calendar_name, "mode", mode or "calendar")

    # Get the events.

    events, shown_events, all_shown_events, earliest, latest = \
        EventAggregatorSupport.getEvents(request, category_names, calendar_start, calendar_end)

    # Get a concrete period of time.

    first, last = EventAggregatorSupport.getConcretePeriod(calendar_start, calendar_end, earliest, latest)

    # Define a view of the calendar, retaining useful navigational information.

    view = View(page, calendar_name, raw_calendar_start, raw_calendar_end,
        original_calendar_start, original_calendar_end, calendar_start, calendar_end,
        first, last, category_names, template_name, parent_name, mode, name_usage)

    # Make a calendar.

    output = []

    # Output download controls.

    output.append(fmt.div(on=1, css_class="event-controls"))
    output.append(view.writeDownloadControls())
    output.append(fmt.div(on=0))

    # Output a table.

    if mode == "table":

        # Start of table view output.

        output.append(fmt.table(on=1, attrs={"tableclass" : "event-table"}))

        output.append(fmt.table_row(on=1))
        output.append(fmt.table_cell(on=1, attrs={"class" : "event-table-heading"}))
        output.append(fmt.text(_("Event dates")))
        output.append(fmt.table_cell(on=0))
        output.append(fmt.table_cell(on=1, attrs={"class" : "event-table-heading"}))
        output.append(fmt.text(_("Event location")))
        output.append(fmt.table_cell(on=0))
        output.append(fmt.table_cell(on=1, attrs={"class" : "event-table-heading"}))
        output.append(fmt.text(_("Event details")))
        output.append(fmt.table_cell(on=0))
        output.append(fmt.table_row(on=0))

        # Get the events in order.

        ordered_events = EventAggregatorSupport.getOrderedEvents(all_shown_events)

        # Show the events in order.

        for event in ordered_events:
            event_page = event.getPage()
            event_summary = event.getSummary(parent_name)
            event_details = event.getDetails()

            # Prepare CSS classes with category-related styling.

            css_classes = ["event-table-details"]

            for topic in event_details.get("topics") or event_details.get("categories") or []:

                # Filter the category text to avoid illegal characters.

                css_classes.append("event-table-category-%s" % "".join(filter(lambda c: c.isalnum(), topic)))

            attrs = {"class" : " ".join(css_classes)}

            output.append(fmt.table_row(on=1))

            # Start and end dates.

            output.append(fmt.table_cell(on=1, attrs=attrs))
            output.append(fmt.span(on=1))
            output.append(fmt.text(str(event_details["start"])))
            output.append(fmt.span(on=0))

            if event_details["start"] != event_details["end"]:
                output.append(fmt.text(" - "))
                output.append(fmt.span(on=1))
                output.append(fmt.text(str(event_details["end"])))
                output.append(fmt.span(on=0))

            output.append(fmt.table_cell(on=0))

            # Location.

            output.append(fmt.table_cell(on=1, attrs=attrs))

            if event_details.has_key("location"):
                output.append(fmt.text(event_details["location"]))

            output.append(fmt.table_cell(on=0))

            # Link to the page using the summary.

            output.append(fmt.table_cell(on=1, attrs=attrs))
            output.append(event_page.linkToPage(request, event_summary))
            output.append(fmt.table_cell(on=0))

            output.append(fmt.table_row(on=0))

        # End of table view output.

        output.append(fmt.table(on=0))

    # Output a list or calendar.

    elif mode in ("list", "calendar"):

        # Output top-level information.

        # Start of list view output.

        if mode == "list":
            output.append(fmt.bullet_list(on=1, attr={"class" : "event-listings"}))

        # Visit all months in the requested range, or across known events.

        for month in first.months_until(last):

            # Either output a calendar view...

            if mode == "calendar":

                # Output a month.

                output.append(fmt.table(on=1, attrs={"tableclass" : "event-month"}))

                output.append(fmt.table_row(on=1))
                output.append(fmt.table_cell(on=1, attrs={"class" : "event-month-heading", "colspan" : "21"}))

                # Either write a month heading or produce links for navigable
                # calendars.

                output.append(view.writeMonthHeading(month))

                output.append(fmt.table_cell(on=0))
                output.append(fmt.table_row(on=0))

                # Weekday headings.

                output.append(fmt.table_row(on=1))

                for weekday in range(0, 7):
                    output.append(fmt.table_cell(on=1, attrs={"class" : "event-weekday-heading", "colspan" : "3"}))
                    output.append(fmt.text(_(EventAggregatorSupport.getDayLabel(weekday))))
                    output.append(fmt.table_cell(on=0))

                output.append(fmt.table_row(on=0))

                # Process the days of the month.

                start_weekday, number_of_days = month.month_properties()

                # The start weekday is the weekday of day number 1.
                # Find the first day of the week, counting from below zero, if
                # necessary, in order to land on the first day of the month as
                # day number 1.

                first_day = 1 - start_weekday

                while first_day <= number_of_days:

                    # Find events in this week and determine how to mark them on the
                    # calendar.

                    week_start = month.as_date(max(first_day, 1))
                    week_end = month.as_date(min(first_day + 6, number_of_days))

                    full_coverage, week_slots = EventAggregatorSupport.getCoverage(
                        week_start, week_end, shown_events.get(month, []))

                    # Output a week, starting with the day numbers.

                    output.append(view.writeDayNumbers(first_day, number_of_days, month, full_coverage))

                    # Either generate empty days...

                    if not week_slots:
                        output.append(view.writeEmptyWeek(first_day, number_of_days))

                    # Or generate each set of scheduled events...

                    else:
                        output.append(view.writeWeekSlots(first_day, number_of_days, month, week_end, week_slots))

                    # Process the next week...

                    first_day += 7

                # End of month.

                output.append(fmt.table(on=0))

            # Or output a summary view...

            elif mode == "list":

                # Output a list.

                output.append(fmt.listitem(on=1, attr={"class" : "event-listings-month"}))
                output.append(fmt.div(on=1, attr={"class" : "event-listings-month-heading"}))

                # Either write a month heading or produce links for navigable
                # calendars.

                output.append(view.writeMonthHeading(month))

                output.append(fmt.div(on=0))

                output.append(fmt.bullet_list(on=1, attr={"class" : "event-month-listings"}))

                # Get the events in order.

                ordered_events = EventAggregatorSupport.getOrderedEvents(shown_events.get(month, []))

                # Show the events in order.

                for event in ordered_events:
                    event_page = event.getPage()
                    event_details = event.getDetails()
                    event_summary = event.getSummary(parent_name)

                    output.append(fmt.listitem(on=1, attr={"class" : "event-listing"}))

                    # Link to the page using the summary.

                    output.append(fmt.paragraph(on=1))
                    output.append(event_page.linkToPage(request, event_summary))
                    output.append(fmt.paragraph(on=0))

                    # Start and end dates.

                    output.append(fmt.paragraph(on=1))
                    output.append(fmt.span(on=1))
                    output.append(fmt.text(str(event_details["start"])))
                    output.append(fmt.span(on=0))
                    output.append(fmt.text(" - "))
                    output.append(fmt.span(on=1))
                    output.append(fmt.text(str(event_details["end"])))
                    output.append(fmt.span(on=0))
                    output.append(fmt.paragraph(on=0))

                    # Location.

                    if event_details.has_key("location"):
                        output.append(fmt.paragraph(on=1))
                        output.append(fmt.text(event_details["location"]))
                        output.append(fmt.paragraph(on=1))

                    # Topics.

                    if event_details.has_key("topics") or event_details.has_key("categories"):
                        output.append(fmt.bullet_list(on=1, attr={"class" : "event-topics"}))

                        for topic in event_details.get("topics") or event_details.get("categories") or []:
                            output.append(fmt.listitem(on=1))
                            output.append(fmt.text(topic))
                            output.append(fmt.listitem(on=0))

                        output.append(fmt.bullet_list(on=0))

                    output.append(fmt.listitem(on=0))

                output.append(fmt.bullet_list(on=0))

        # Output top-level information.

        # End of list view output.

        if mode == "list":
            output.append(fmt.bullet_list(on=0))

    # Output view controls.

    output.append(fmt.div(on=1, css_class="event-controls"))
    output.append(view.writeViewControls())
    output.append(fmt.div(on=0))

    return ''.join(output)

# vim: tabstop=4 expandtab shiftwidth=4
