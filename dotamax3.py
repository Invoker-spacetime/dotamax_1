#dotamax3.py

from hero_rate import hero
import time
from multiprocessing import Pool
import os
from sql_hero import hero_sql
import json

def pickle_search(hero_name_p,rate_all):
		return hero(hero_name_p,rate_all).search_hero_rate()

def Nice_Best_Hero(teammate_list,opponent_list):

	rate_point = 0
	rate_max = -100
	best_hero = 'Nobody'
	len_team = len(teammate_list)
	len_opps = len(opponent_list)
	for hero_iter in hero_list:  
		rate_team  =   rate_opps = com_rate = 0.0
		if ((hero_iter in teammate_list)|(hero_iter in opponent_list)) == False:
			for team_iter in teammate_list:        
				rate_team_p = hero_sql().search_hero_sql(hero_iter,team_iter,'Nobody') 
				rate_team = rate_team_p + rate_team
				print 'team_rate',hero_iter,team_iter,rate_team_p
			for opps_iter in opponent_list:
				rate_opps_p = hero_sql().search_hero_sql(hero_iter,'Nobody',opps_iter) 
				rate_opps = rate_opps_p + rate_opps
				print 'opp_rate',hero_iter,opps_iter,rate_opps_p
			if  len_team + len_opps == 0:
				raise
			elif len_team == 0:
				com_rate = (rate_opps/len_opps) - float(hero_rate_dict[hero_iter])
			elif len_opps == 0:
				com_rate = (rate_team/len_team) - float(hero_rate_dict[hero_iter])
			else:
				com_rate = (rate_team/len_team + rate_opps/len_opps)/2 - float(hero_rate_dict[hero_iter])
						
			if (com_rate) > rate_max:
				rate_max = com_rate 
				best_hero = hero_iter

			print '%.2f\t%.2f\t%s\r\n'%(com_rate,float(hero_rate_dict[hero_iter]),hero_iter)
	return best_hero,rate_max

start_time  = time.time()

#

#get hero list


if 1: #get databass,sometimes dont use
	try:
		os.remove('hero_list.txt')
		os.remove('hero_rate_dict.txt')
		os.remove('hero_url_dict.txt')
		os.remove('my_hero.db')		
	except Exception, e:
		raise e
	finally:
		pass

	hero_sql().init_sql()
	hero_list , hero_rate_dict , hero_url_dict= hero('all').get_main_hero() #get hero list
	with open ('hero_list.txt','wb') as f:
		f.write(json.dumps(hero_list))
	with open ('hero_rate_dict.txt','wb') as f:
		f.write(json.dumps(hero_rate_dict))
	with open ('hero_url_dict.txt','wb') as f:
		f.write(json.dumps(hero_url_dict))

	#print 'Parent process %s.' % os.getpid()
	p = Pool(4)
	for i in hero_list:
		p.apply_async(pickle_search , args = (i,hero_rate_dict[i]))
		#pickle_search(i,hero_rate_dict[i])#204.154642
			#print 'Waiting for all subprocesses done...'
	p.close()
	p.join()
	#print 'All subprocesses done.'
else:
	hero_sql().init_sql()
	with open ('hero_list.txt','wb') as f:
		hero_list = json.loads(f.read())
	with open ('hero_rate_dict.txt','wb') as f:
		hero_rate_dict= json.loads(f.read())
	with open ('hero_url_dict.txt','wb') as f:
		hero_url_dict = json.loads(f.read())

team_list = ['Omniknight']
opps_list = []
#"Bounty Hunter", "Weaver", "Jakiro", "Batrider"
print 'Hero name: %s\t Hero fit:%s'%(Nice_Best_Hero(team_list,opps_list))
#print hero_rate_dict
#print (Lina_comb)
#print (Lina_anti)
'''  
for n in Lina:
	print 'hero_name: %s  hero_rate: %s'%(n.hero_name,n.hero_rate)
for n in Lina_comb:
	print 'hero_name: %s  hero_comb_name: %s team_rate: %s'%(n.hero_name,n.hero_comb_name,n.team_rate)
for n in Lina_anti:
	print 'hero_name: %s  hero_anti_name: %s beat_rate: %s'%(n.hero_name,n.hero_anti_name,n.beat_rate)
#print (Lina.hero_name,Lina.hero_rate,Lina.hero_anti_rate)
'''
print('Cost time:%f'%(time.time() - start_time))



