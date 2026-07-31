#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <stdexcept>
#include <tuple>
#include <vector>
#ifdef _OPENMP
#include <omp.h>
#endif
using namespace std;
constexpr int MAXW = 16;
struct Mask { array<uint64_t, MAXW> w{}; };
struct Desc { int p,l,r,f; auto key() const {return tuple<int,int,int,int>(p,l,r,f);} bool operator<(const Desc&o)const{return key()<o.key();} bool operator==(const Desc&o)const{return key()==o.key();}};
struct Block {Desc d; Mask active;}; struct Cell {uint16_t prefix; Mask rows;};
int NVAR,MOUT,NROWS,WORDS; vector<Block> BLOCKS;
inline Mask intersect_mask(const Mask&a,const Mask&b){Mask r;for(int i=0;i<WORDS;i++)r.w[i]=a.w[i]&b.w[i];return r;}
inline Mask difference_mask(const Mask&a,const Mask&b){Mask r;for(int i=0;i<WORDS;i++)r.w[i]=a.w[i]&~b.w[i];return r;}
inline int popcount_mask(const Mask&a){int s=0;for(int i=0;i<WORDS;i++)s+=__builtin_popcountll(a.w[i]);return s;}
inline int required_extensions(int fixed,int zeros){if(zeros>2)return 0;int rem=MOUT-fixed,budget=2-zeros;if(budget==0)return 1;if(budget==1)return 1+rem;return 1+rem+rem*(rem-1)/2;}
Desc normalize_desc(int p,int l,int r,int f){if(l<r)return{p,l,r,f};int ff=(f==1?2:(f==2?1:3));return{p,r,l,ff};}
Desc transform_desc(const Desc&d,const vector<int>&perm){return normalize_desc(perm[d.p],perm[d.l],perm[d.r],d.f);}
vector<Block> generate_blocks(int n,int canonical_f){vector<Block>all;for(int p=0;p<n;p++){vector<int>others;for(int v=0;v<n;v++)if(v!=p)others.push_back(v);for(int a=0;a<(int)others.size();a++)for(int b=a+1;b<(int)others.size();b++){int l=others[a],r=others[b];for(int f=1;f<=3;f++){Mask mask;for(int x=0;x<(1<<n);x++){if((x>>p)&1)continue;int pair=((x>>l)&1)|(((x>>r)&1)<<1);if(pair!=f)mask.w[x>>6]|=1ULL<<(x&63);}all.push_back({{p,l,r,f},mask});}}}sort(all.begin(),all.end(),[](const Block&a,const Block&b){return a.d<b.d;});Desc first{0,1,2,canonical_f};auto it=find_if(all.begin(),all.end(),[&](const Block&b){return b.d==first;});Block canonical=*it;all.erase(it);all.insert(all.begin(),canonical);return all;}
vector<int> second_orbit_representatives(int n,int canonical_f){vector<int>freevars;for(int v=3;v<n;v++)freevars.push_back(v);vector<vector<int>>stabilizer;sort(freevars.begin(),freevars.end());do{vector<int>p(n);iota(p.begin(),p.end(),0);for(int i=0;i<(int)freevars.size();i++)p[3+i]=freevars[i];stabilizer.push_back(p);if(canonical_f==3){auto q=p;swap(q[1],q[2]);stabilizer.push_back(q);}}while(next_permutation(freevars.begin(),freevars.end()));map<Desc,int>rep;for(int idx=1;idx<(int)BLOCKS.size();idx++){Desc canon=BLOCKS[idx].d;for(const auto&p:stabilizer)canon=min(canon,transform_desc(BLOCKS[idx].d,p));auto it=rep.find(canon);if(it==rep.end()||BLOCKS[idx].d<BLOCKS[it->second].d)rep[canon]=idx;}vector<int>res;for(auto&kv:rep)res.push_back(kv.second);return res;}
struct Searcher{long long nodes=0,node_limit;atomic<bool>*found;vector<int>solution;vector<char>chosen;bool recurse(int fixed,int start,const vector<Cell>&cells,vector<int>&selection){if(found->load(memory_order_relaxed))return false;if(++nodes>node_limit)throw runtime_error("node limit exceeded");if(fixed==MOUT){solution=selection;found->store(true);return true;}struct Candidate{int idx,slack;vector<Cell>cells;};vector<Candidate>candidates;for(int idx=start;idx<(int)BLOCKS.size();idx++){if(chosen[idx])continue;bool ok=true;int slack=0;vector<Cell>next;next.reserve(cells.size()*2);for(const auto&c:cells){int zeros=fixed-__builtin_popcount((unsigned)c.prefix);Mask yes=intersect_mask(c.rows,BLOCKS[idx].active);Mask no=difference_mask(c.rows,BLOCKS[idx].active);int ry=required_extensions(fixed+1,zeros),rn=required_extensions(fixed+1,zeros+1);int cy=popcount_mask(yes),cn=popcount_mask(no);if(cy<ry||cn<rn){ok=false;break;}if(ry)next.push_back({(uint16_t)((c.prefix<<1)|1),yes});if(rn)next.push_back({(uint16_t)(c.prefix<<1),no});slack+=cy-ry+cn-rn;}if(ok)candidates.push_back({idx,slack,move(next)});}sort(candidates.begin(),candidates.end(),[](const Candidate&a,const Candidate&b){return a.slack<b.slack;});for(auto&c:candidates){chosen[c.idx]=1;selection.push_back(c.idx);if(recurse(fixed+1,c.idx+1,c.cells,selection))return true;selection.pop_back();chosen[c.idx]=0;if(found->load())return false;}return false;}};
struct SearchResult{bool found=false,complete=true;long long nodes=0;vector<Desc>solution;};
SearchResult search_case(int n,int canonical_f,long long branch_limit,int threads){NVAR=n;MOUT=n+1;NROWS=1<<n;WORDS=(NROWS+63)/64;BLOCKS=generate_blocks(n,canonical_f);auto reps=second_orbit_representatives(n,canonical_f);Mask full;for(int i=0;i<WORDS;i++)full.w[i]=~0ULL;if(NROWS%64)full.w[WORDS-1]=(1ULL<<(NROWS%64))-1;vector<Cell>first={{1,BLOCKS[0].active},{0,difference_mask(full,BLOCKS[0].active)}};struct Top{int idx;vector<Cell>cells;};vector<Top>tops;for(int idx:reps){bool ok=true;vector<Cell>next;for(const auto&c:first){int zeros=1-__builtin_popcount((unsigned)c.prefix);Mask yes=intersect_mask(c.rows,BLOCKS[idx].active),no=difference_mask(c.rows,BLOCKS[idx].active);int ry=required_extensions(2,zeros),rn=required_extensions(2,zeros+1);if(popcount_mask(yes)<ry||popcount_mask(no)<rn){ok=false;break;}if(ry)next.push_back({(uint16_t)((c.prefix<<1)|1),yes});if(rn)next.push_back({(uint16_t)(c.prefix<<1),no});}if(ok)tops.push_back({idx,move(next)});}atomic<bool>found(false);
#ifdef _OPENMP
omp_set_num_threads(threads);int slots=threads;
#else
int slots=1;
#endif
vector<long long>counts(slots,0);vector<char>complete(slots,1);vector<vector<int>>answers(slots);
#pragma omp parallel for schedule(dynamic,1) if(threads>1)
for(int q=0;q<(int)tops.size();q++){if(found.load())continue;
#ifdef _OPENMP
int tid=omp_get_thread_num();
#else
int tid=0;
#endif
Searcher s;s.node_limit=branch_limit;s.found=&found;s.chosen.assign(BLOCKS.size(),0);s.chosen[0]=s.chosen[tops[q].idx]=1;vector<int>selection={0,tops[q].idx};try{s.recurse(2,1,tops[q].cells,selection);}catch(const runtime_error&){complete[tid]=0;}counts[tid]+=s.nodes;if(!s.solution.empty())answers[tid]=s.solution;}
SearchResult result;result.found=found.load();result.complete=all_of(complete.begin(),complete.end(),[](char c){return c!=0;});result.nodes=accumulate(counts.begin(),counts.end(),0LL);if(result.found)for(const auto&a:answers)if(!a.empty()){for(int idx:a)result.solution.push_back(BLOCKS[idx].d);break;}return result;}
int main(int argc,char**argv){int min_n=argc>1?stoi(argv[1]):3,max_n=argc>2?stoi(argv[2]):9;long long lim=argc>3?stoll(argv[3]):500000000LL;int threads=argc>4?stoi(argv[4]):8;cout<<"n,canonical_type,found_counterexample,complete,nodes\n";int only_f=argc>5?stoi(argv[5]):0;for(int n=min_n;n<=max_n;n++)for(int f:{1,3}){if(only_f && f!=only_f) continue;auto r=search_case(n,f,lim,threads);cout<<n<<','<<f<<','<<(r.found?1:0)<<','<<(r.complete?1:0)<<','<<r.nodes<<"\n";if(r.found){cerr<<"counterexample n="<<n<<" f="<<f<<':';for(auto&d:r.solution)cerr<<" ("<<d.p<<','<<d.l<<','<<d.r<<','<<d.f<<')';cerr<<'\n';return 2;}if(!r.complete)return 3;}return 0;}
