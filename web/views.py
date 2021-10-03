from django.http import HttpResponse
# Create your views here.
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
from rdkit.Chem.Draw.MolDrawing import MolDrawing, DrawingOptions #Only needed if modifying defaults
from web import db
import json
from rdkit.Chem import DataStructs
import os

from web import sim

def index(request):
    json_data = ""
    return HttpResponse(json_data, content_type="application/json")


def test(request):
    data = db.getSql()
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json")

def result(request):
    type = request.GET.get("type")
    query = request.GET.get("query")

    try:

        # 初始化
        if query == None or type == None or query == "":
            return HttpResponse("", content_type="application/json")
            
        data = "" 
        # 查询
        if type == "1":
            query = canonicalize_smiles(query)
            sql = "select Pubchem_CID,Category,Subcategory,Compound_Name,SMILES from substrate where canonical_substrate_smiles='"+query+"'"
            image = dopic(query)
            data = db.getAllSql(sql)
            for v in  data:
                v['image'] = image


        
        # 相似度
        elif type == "2":
            sql = "select Pubchem_CID,Category,Subcategory,Compound_Name,SMILES from substrate"
            outdata = []
            data = db.getAllSql(sql)
            if data != None:
                for v in  data:
                    image = dopic(v['SMILES'])
                    v['image'] = image
                    v['score'] = do_sim(query,v['SMILES'])
                    flag = 0
                    if len(outdata) == 0:
                        outdata.append(v)
                        flag=1
                    for oi in range (0,len(outdata)-1):
                        if outdata[oi]['score'] > v['score'] and outdata[oi+1]['score']<v['score']:
                            outdata.insert(oi+1,v)
                            flag = 1
                            break
                    if flag==0 and outdata[0]['score']<v['score']:
                        outdata.insert(0,v)
                        flag = 1
                    else:
                        if flag == 0:
                            outdata.append(v)       
                data = outdata[:20]
            else:
                data = ""




        # 预测
        elif type == "3":
            mylist,mymap = sim.forecast(query)
            data = []
            for v in mylist:
                outdic = {}
                outdic['react_product'] = v
                outdic['score'] = mymap[v]
                image = dopic(v)
                outdic['image'] = image
                data.append(outdic)

        elif type == "4":
            #1-chloro-2,4-dinitrobenzene
            sql = "select Pubchem_CID,Category,Subcategory,Compound_Name,SMILES from substrate where Compound_Name like '%"+query+"%' or Compound_Name like '%"+query+"%'"
            data = db.getAllSql(sql)
            if data!=None and len(data)!=0:
                smile = data[0]['SMILES']
                smile = canonicalize_smiles(smile)
                image = dopic(smile)
                data[0]['image'] = image
            

        json_data = json.dumps(data)
    except Exception as err:
        print(err,"corey")
        return HttpResponse("error", content_type="application/json")
    return HttpResponse(json_data, content_type="application/json")

    
def detail(request):
    try:
        outdata = []
        id = request.GET.get("id")
        json_data = ""
        if id == None:
            return HttpResponse(json_data, content_type="application/json")
        sql = "select Category,Subcategory,Compound_Name,SMILES,Canonical_SMILES,INCHI,INCHIKEY,Molecular_Weight,LogP,H_bond_acceptors,Topological_Polar_Surface_Area from substrate where Pubchem_CID='"+id+"' limit 1"
        mydata = db.getSql(sql)
        if mydata!=None:
            smile = mydata['SMILES']
            smile = canonicalize_smiles(smile)
            image = dopic(smile)
            mydata['image'] = image
        sql = "select Substrate,Substrate_SMILES,Reaction_class,Reaction_type,Product,Product_SMLIE,Enzyme,Reference,Major_product,Biosystem from biotransformation_reactions where Pubchem_CID='"+id+"'"
        data = db.getAllSql(sql)
        for v in data:
            br_smile =  canonicalize_smiles(v['Substrate_SMILES'])
            br_smile = canonicalize_smiles(br_smile)
            image = dopic(br_smile)
            v['image'] = image

        mydata['ext'] = data
        json_data = json.dumps(mydata)
    except Exception as err:
        print(err)
        return HttpResponse("", content_type="application/json")
    return HttpResponse(json_data, content_type="application/json")


def dopic(query):
    outfile = query.replace("/","")
    picname = outfile+'.jpg'
    filename = "./media/"+outfile+".jpg"
    if os.path.isfile(filename):
        print("exist")
        return "http://1.117.57.232:8080/media/"+picname
    
    opts = DrawingOptions()
    # 'OC1C2C1CC2'
    m = Chem.MolFromSmiles(query)
    opts.includeAtomNumbers=True
    opts.bondLineWidth=2.8
    draw = Draw.MolToImage(m, options=opts)
    draw.save('./media/'+outfile+'.jpg')
  
    return "http://1.117.57.232:8080/media/"+picname


def canonicalize_smiles(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is not None:
        return Chem.MolToSmiles(mol, isomericSmiles=True)
    else:
        return ''


def do_sim(str1,str2):
    m1 = Chem.MolFromSmiles(str1)
    m2 = Chem.MolFromSmiles(str2)
    fp1 = AllChem.GetMorganFingerprint(m1,2)
    fp2 = AllChem.GetMorganFingerprint(m2,2)
    return DataStructs.TanimotoSimilarity(fp1,fp2)