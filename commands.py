import time
from datetime import datetime
from arxivreader import all_arxiv_section

avail_sites = ["arxiv"]
avail_section = {"arxiv":all_arxiv_section}

class paper_command:
    def __init__(self, call="paper", site=["arxiv"],
                 sections=[], span=1, begin=None, end=None, kw=[], authors=[]):
        self.call = call
        self.site = site
        if isinstance(sections, str):
            sections = [sections]
        self.section = sections
        self.span = span
        self.begin = begin
        self.end = end
        if isinstance(kw, str):
            kw = [kw]
        self.kw = kw
        if isinstance(authors, str):
            authors = [authors]
        self.authors = authors

    def __eq__(self, other):
        return self.call == other

    def N(self, span):
        error_msg = ""
        if isinstance(span, int):
            return span
        elif span == "week":
            wdays_dict  = {'Sun': 7, 'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6}
            today_char  = datetime.now().strftime('%a')
            return wdays_dict[today_char]
        elif span == "month":
            today = time.strftime("%Y-%m-%d")
            return int(today[8:])
        else:
            try:
                N = int(span)
            except:
                error_msg += "Span not understood\n"
                N = 1
            return N, error_msg

    def __call__(self, args):
        N = self.N(self.span)
        sites = []
        sections = self.section
        begin = self.begin
        end = self.end
        kw = self.kw
        authors = self.authors

        error_msg = ""

        args_list = []
        if "[" in args:
            args += " "
            split_brace = args.replace("[","]").split("]")
            if len(split_brace) %2 == 0:
                error_msg += "Square bracket not closed\n"
            for i in range(0,len(split_brace),2):
                split_space = split_brace[i].split()
                for arg in split_space:
                    split_eq = arg.split('=')
                    if len(split_eq) == 2:
                        if split_eq[1]:
                            args_list.append((split_eq[0], split_eq[1]))
                        else:
                            val = split_brace[i+1].split(",")
                            val = [v.strip() for v in val]
                            args_list.append((split_eq[0], val))
                    else:
                        error_msg += "Could not understand args\n"
        else:
            split_space = args.split()
            for arg in split_space:
                split_eq = arg.split('=')
                if len(split_eq) == 2:
                    args_list.append((split_eq[0], split_eq[1]))
                else:
                    error_msg += "Could not understand args\n"

        for arg, val in args_list:
            if arg.startswith("site"):
                sites = val if isinstance(val, list) else [val]
            elif arg.startswith("sections"):
                sections = val if isinstance(val, list) else [val]
            elif arg.startswith("begin"):
                begin = val
            elif arg.startswith("end"):
                end = val
            elif arg.startswith("kw") or arg.startswith("keyword"):
                kw = val if isinstance(val, list) else [val]
            elif arg.startswith("author"):
                authors = val if isinstance(val, list) else [val]
            elif arg.startswith("span"):
                N, err = self.N(val)
                error_msg += err
            else:
                error_msg += "args '" + arg +"' not understood\n"

        if sites:
            used_sites = []
            for site in sites:
                if site in avail_sites:
                    used_sites.append(site)
                else:
                    error_msg += "unknown site: " + site +"\n"
        else:
            used_sites = self.site

        used_sections = {}
        for site in used_sites:
            used_sections[site] = []
        for section in sections:
            for site in used_sites:
                if section in avail_section[site]:
                    used_sections[site].append(section)
                    break
            else:
                error_msg += "section '" + section + \
                             "' does not match any known section\n"

        try:
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
        except:
            if end is not None:
                error_msg += "Could not understand the end date\n"
            end = time.strftime("%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d").date()

        try:
            begin_date = datetime.strptime(begin, "%Y-%m-%d").date()
            N = (end_date - begin_date).days + 1
        except:
            if begin is not None:
                error_msg += "Could not understand the begining date\n"

        outlist = []
        for site in used_sites:
            outlist.append((site, (end, N, used_sections[site], kw, authors)))
        print(outlist)
        return outlist, error_msg

    def help(self):
        text = self.call + ": Print paper from " + " ".join(self.site) + ":" + " ".join(self.section) +"\n"
        if self.kw:
            text += "    For the keywords "+ ", ".join(self.kw) +"\n"
        if self.authors:
            text += "    For the authors "+ ", ".join(self.kw) +"\n"
        if self.begin:
            text += "    From " + str(self.begin) + " until "
            if not self.end:
                text += "today"
            else:
                text += str(self.end)
        else:
            if not self.end:
                if self.span == "week":
                    text += "    For the week"
                elif self.span == "month":
                    text += "    For the month"
                else:
                    N = self.N(self.span)
                    if N == 1:
                        text += "    For the day"
                    else:
                        text += "    For the last " + str(N) + "days"
            else:
                N = self.N(self.span)
                text += "    For " + str(N) + "days before the " + str(self.end)
        return text


def create_commands(def_name, default_sections, home_commands):
    paper_command_list = []
    paper_command_list.append(paper_command(call=def_name, sections=default_sections))
    for hc_name, hc_args in home_commands:
        if not "sections" in hc_args:
            hc_args["sections"] = default_sections
        paper_command_list.append(paper_command(call=hc_name, **hc_args))
        """try:
            paper_command_list.append(paper_command(call=hc_name, **hc_args))
        except:
            pass"""
    return paper_command_list
