# moin198-git

MoinMoin데이타를 git에서 관리하기. 간단한 컨셉입니다.

 1. MoinMoin 코드를 최소한으로 수정하기
 2. 기존 사용하던 MoinMoin에 간단히 붙이고 빼기
 3. 첨부파일까지 지원

사용방법:  moin.py 스크립트를 이용합니다.
```
moin.py git init
moin.py git page2git
cd $WIKI_DIR/pages
git push <remote>
```

구현하다보니 몇가지 이슈가 있었습니다.
 
 1. 기본적으로 working-directory가 있는 repo에 push가 안되어서 구현 방향 자체를 고민했음. bare를 따로 만들고 양쪽에서 pull/push하는게 너무 번거로울 것 같았고, 용량적인 측면에서도 배로 차지하니까 효율적이지 않은 느낌이었는데 다행히 방법이 있었고 ***Push를 하면 자동으로 update까지 되니까 mercurial보다 품이 덜 드는 점이 마음에 든다. 오히려 더 좋아졌다.***
 2. MoinMoin의 파일저장소인 pages 디렉토리 자체를 git repo로 잡았는데 별도로 페이지파일 관리는 필요하겠다 싶어서 각 페이지 디렉토리 이름과 동일한 md파일을 하나씩 생성. git에 hook을 걸어서 update시점마다 git2page를 수행하는 구조. RecentChanges에 보이지만 문서 작성시점은 아니고 fetch시점으로 잡히지만 이 정도는 감수해도 될 것으로 보임.
 3. 한글로 된 첨부파일이 git에서 잘 인식이 안되는 문제가 있습니다. (윈도우즈는 테스트되지 않음)
 4. cleanpage를 하면 .git을 없애려고 하기 때문에 .git 저장소는 pages와 동일한 레벨의 pages.git이라는 디렉토리 이름으로 관리.
 5. MoinMoin.scripts에 다음 명령어들을 추가.
  - moin.py git init
  - moin.py git remove
  - moin.py git page2git
  - moin.py git git2page

해결되지 않은 이슈들
 1. page2git을 할 경우 첨부파일에 대해 기존에 repo에 포함되어있는지를 확인할 수가 없기 때문에 항상 staged되는 문제가 있다.
 2. 삭제처리가 완전하지 않다. ('''이 때문에 git에서 데이타수정할때에는 삭제는 하지 않는 것이 좋겠다.''')
  1. git에서 파일삭제할 경우는 MoinMoin에서의 tracking이 어렵다. 동기화시 물리 파일과의 차이를 보고 삭제할 수도 있지만 위험한 편이다.
  1. 한글이름의 첨부파일삭제가 잘 동작하지 않는다.

gunicorn을 이용해서 위키인스턴스와 git서버를 같이 띄우기

```python
# -*- coding: utf-8 -
from werkzeug.wsgi import DispatcherMiddleware
from MoinMoin.web.serving import make_application
from MoinMoin.support.gitweb import GitDirectory
import os

from farmconfig import wikis

include = [ wiki for wiki, url in wikis ]

config = {x: __import__(x) for x in include}
gits_dir = {x: os.path.join(config[x].Config.data_dir, 'pages') for x in include}
gits_is  = {x: GitDirectory(gits_dir[x], auto_create=True) for x in include}

shared = '/Users/happytk/Dev/moin198/MoinMoin/web/static/htdocs'
app = make_application(shared)

urlmap = {'/'+x[5:]:app for x in include}
urlmap.update({'/' + x[5:] + '.git':gits_is[x] for x in include})

app = DispatcherMiddleware(app, urlmap)
```