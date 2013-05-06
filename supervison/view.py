import web
t_globals = dict(
  datestr=web.datestr,
  str=str,
  type=type
)

render = web.template.render('templates/', globals=t_globals)
render._keywords['globals']['render'] = render

if __name__=='__main__':
    print t_globals
