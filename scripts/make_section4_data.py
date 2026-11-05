"""Section IV evidence: one row per evaluated driving scene (reference provenance, target size, metadata).

Usage: python3 scripts/make_section4_data.py evals/data/04_scene_inventory.csv
Standard library only; reads (never writes) /home/william/data:
  gaze_accuracy/offset/units/units_driving.csv              evaluated scenes (unit_id = recording UUID/event UUID)
  driving/recordings/<rec>/detections.json                   target boxes, localisation source/method, validation flag
  driving/recordings/<rec>/scene_metadata.json, info.json    scene tags, session conditions, recording identity
Box height/width: median over frames inside the fixation (fixation_active not False) with a valid target box.
src_*: frames per localisation source (manual / tracking / model / unknown); method: tracker name and frame count.
"""
import json,csv,collections,statistics as st,sys
D='/home/william/data'
U=[u for u in csv.DictReader(open(f'{D}/gaze_accuracy/offset/units/units_driving.csv'))]
recs=sorted({u['recording_name'] for u in U})
out=[]
for r in recs:
    det=json.load(open(f'{D}/driving/recordings/{r}/detections.json'))
    meta=json.load(open(f'{D}/driving/recordings/{r}/scene_metadata.json'))
    info=json.load(open(f'{D}/driving/recordings/{r}/info.json'))
    rid=info['recording_id']
    mev={e['event_id']:e for e in meta['events']}
    frames=collections.defaultdict(list); validated={}
    if 'events' in det:
        for ev in det['events']:
            validated[ev['event_id']]=ev.get('validated')
            for f in ev['frames']: frames[ev['event_id']].append(f)
    else:
        for f in det['frames']:
            a=f.get('annotation') or {}; m=a.get('metadata') or {}
            if m.get('event_id'):
                frames[m['event_id']].append(f); validated[m['event_id']]=m.get('event_validated')
    for u in [u for u in U if u['recording_name']==r]:
        eid=u['unit_id'].split('/')[1]; fs=frames.get(eid,[]); e=mev.get(eid,{})
        hs=[];ws=[];src=collections.Counter();meth=collections.Counter();act=0
        for f in fs:
            a=f.get('annotation') or {}; oid=a.get('object_id')
            o=(f.get('objects') or {}).get(oid)
            am=a.get('metadata') or {}
            if am.get('fixation_active') is False: continue
            act+=1
            if o and o.get('box') and o.get('valid',True):
                b=o['box']; hs.append(b[3]-b[1]); ws.append(b[2]-b[0])
                m=o.get('metadata') or {}; src[m.get('source') or (f.get('detector_metadata') or {}).get('source')]+=1; meth[m.get('method') or ''] +=1
        out.append(dict(participant=u['participant'],recording=r,event_id=eid,label=u['label'],cls=e.get('target',{}).get('class'),subtype=e.get('target',{}).get('subtype'),
            validated=validated.get(eid),player_validated=u.get('player_validated'),frames=len(fs),active_frames=act,boxed_active=len(hs),
            box_h_med=st.median(hs) if hs else None,box_w_med=st.median(ws) if ws else None,
            src_manual=src.get('manual',0),src_tracking=src.get('tracking',0),src_model=src.get('model',0),src_unknown=src.get('unknown',0)+src.get(None,0),
            method=';'.join(f"{k}:{v}" for k,v in meth.items() if k),
            distance_m=e.get('distance_m',{}).get('mean') if e.get('distance_m') else None, distance_source=e.get('distance_source'),
            ego_motion=e.get('ego',{}).get('motion'), speed_kmh=(e.get('ego',{}).get('speed_kmh') or {}).get('mean'), speed_source=e.get('ego',{}).get('speed_source'),
            relative_motion=e.get('relative_motion'), target_motion=e.get('target',{}).get('motion'), side=e.get('target',{}).get('side'),
            road=e.get('road',{}).get('type'), view=e.get('view'), exposure=e.get('image',{}).get('gaze_exposure'), issues='|'.join(e.get('image',{}).get('issues') or []),
            weather=meta.get('session',{}).get('weather'), light=meta.get('session',{}).get('light'), observer=meta.get('observer_role'),
            reviewed_by=(meta.get('provenance') or {}).get('reviewed_by'), date=info.get('start_time')))
w=csv.DictWriter(open(sys.argv[1] if len(sys.argv) > 1 else 'evals/data/04_scene_inventory.csv','w',newline=''),fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out))
