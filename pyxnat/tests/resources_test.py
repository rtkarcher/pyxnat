import os
import tempfile
from uuid import uuid1

from ..pyxnat import Interface

_modulepath = os.path.dirname(os.path.abspath(__file__))

central = Interface('http://central.xnat.org', 'nosetests', 'nosetests')

_id_set1 = {
    'sid':uuid1().hex,
    'eid':uuid1().hex,
    'aid':uuid1().hex,
    'cid':uuid1().hex,
    'rid':uuid1().hex,
    }

_id_set2 = {
    'sid':uuid1().hex,
    'eid':uuid1().hex,
    'aid':uuid1().hex,
    'cid':uuid1().hex,
    'rid':uuid1().hex,
    }

subj_1 = central.select.project('nosetests').subject(_id_set1['sid'])
expe_1 = subj_1.experiment(_id_set1['eid'])
asse_1 = expe_1.assessor(_id_set1['aid'])
scan_1 = expe_1.scan(_id_set1['cid'])
reco_1 = expe_1.reconstruction(_id_set1['rid'])

def test_subject_create():
    assert not subj_1.exists()
    subj_1.create()
    assert subj_1.exists()

def test_experiment_create():
    assert not expe_1.exists()
    expe_1.create()
    assert expe_1.exists()

def test_assessor_create():
    assert not asse_1.exists()
    asse_1.create()
    assert asse_1.exists()

def test_scan_create():
    assert not scan_1.exists()
    scan_1.create()
    assert scan_1.exists()

def test_reconstruction_create():
    assert not reco_1.exists()
    reco_1.create()
    assert reco_1.exists()

def test_multi_create():
    asse_2 = central.select('/projects/nosetests/subjects/%(sid)s'
                              '/experiments/%(eid)s/assessors/%(aid)s'%_id_set2
                              )

    expe_2 = central.select('/projects/nosetests/subjects/%(sid)s'
                              '/experiments/%(eid)s'%_id_set2
                              )

    assert not asse_2.exists()
    asse_2.create(experiments='xnat:petSessionData',                
                  assessors='xnat:petAssessorData')
    assert asse_2.exists()

    assert asse_2.datatype() == 'xnat:petAssessorData'
    assert expe_2.datatype() == 'xnat:petSessionData'

    scan_2 = central.select('/projects/nosetests/subjects/%(sid)s'
                              '/experiments/%(eid)s/scans/%(cid)s'%_id_set2
                              ).create()

    assert scan_2.datatype() == 'xnat:mrScanData'

#def test_share_subject():
#    assert not central.select('/projects/nosetests2/subjects/%(sid)s'%_id_set1
#                              ).exists()
#    subj_1.share('nosetests2')
#    assert central.select('/projects/nosetests2/subjects/%(sid)s'%_id_set1
#                              ).exists()
#    assert set(subj_1.shares().get()) == set(['nosetests', 'nosetests2'])

#def test_share_experiment():
#    assert not central.select('/projects/nosetests2/subjects/%(sid)s'
#                          '/experiments/%(eid)s'%_id_set1
#                          ).exists()
#    expe_1.share('nosetests2')
#    assert central.select('/projects/nosetests2/subjects/%(sid)s'
#                          '/experiments/%(eid)s'%_id_set1
#                          ).exists()
#    assert set(expe_1.shares().get()) == set(['nosetests', 'nosetests2'])

#def test_share_assessor():
#    assert not central.select('/projects/nosetests2/subjects/%(sid)s'
#                              '/experiments/%(eid)s/assessors/%(aid)s'%_id_set1
#                              ).exists()
#    asse_1.share('nosetests2')
#    assert central.select('/projects/nosetests2/subjects/%(sid)s'
#                          '/experiments/%(eid)s/assessors/%(aid)s'%_id_set1
#                          ).exists()
#    assert set(asse_1.shares().get()) == set(['nosetests', 'nosetests2'])

#def test_unshare_assessor():
#    asse_1.unshare('nosetests2')
#    assert not central.select('/projects/nosetests2/subjects/%(sid)s'
#                              '/experiments/%(eid)s/assessors/%(aid)s'%_id_set1
#                              ).exists()
#    assert asse_1.shares().get() == ['nosetests']

#def test_unshare_experiment():
#    expe_1.unshare('nosetests2')
#    assert not central.select('/projects/nosetests2/subjects/%(sid)s'
#                          '/experiments/%(eid)s'%_id_set1
#                          ).exists()
#    assert expe_1.shares().get() == ['nosetests']

#def test_unshare_subject():
#    subj_1.unshare('nosetests2')
#    assert not central.select('/projects/nosetests2/subjects/%(sid)s'%_id_set1
#                              ).exists()
#    assert subj_1.shares().get() == ['nosetests']

def test_put_file():
    local_path = os.path.join(_modulepath, 'hello_xnat.txt')
    subj_1.resource('test').file('hello.txt').put(local_path)
    assert subj_1.resource('test').file('hello.txt').exists()
    assert long(subj_1.resource('test').file('hello.txt').size()) == \
                                                os.stat(local_path).st_size

def test_get_file():
    fpath = subj_1.resource('test').file('hello.txt').get()
    assert os.path.exists(fpath)
    assert open(fpath, 'rb').read() == 'Hello XNAT!\n'

def test_get_copy_file():   
    fpath = subj_1.resource('test').file('hello.txt').get_copy(os.path.join(tempfile.gettempdir(), uuid1().hex))
    assert os.path.exists(fpath)
    fd = open(fpath, 'rb')
    assert fd.read() == 'Hello XNAT!\n'
    fd.close()
    os.remove(fpath)

def test_subject1_delete():
    assert subj_1.exists()
    subj_1.delete()
    assert not subj_1.exists()

def test_subject2_delete():
    subj_2 = central.select('/projects/nosetests/subjects/%(sid)s'%_id_set2)
    assert subj_2.exists()
    subj_2.delete()
    assert not subj_2.exists()
