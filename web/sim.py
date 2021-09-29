import argparse

import pandas as pd
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import AllChem
from rdkit.Chem import rdChemReactions


def get_similarity_1(smi1, smi2):
    """
    计算similarity
    """
    fp1 = AllChem.GetMorganFingerprint(Chem.MolFromSmiles(smi1), 2)
    fp2 = AllChem.GetMorganFingerprint(Chem.MolFromSmiles(smi2), 2)
    similarity = DataStructs.TanimotoSimilarity(fp1, fp2)
    return similarity


def canonicalize_smiles(smiles):
    """
    apply template
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is not None:
        return Chem.MolToSmiles(mol, isomericSmiles=True)
    else:
        return ''


def forecast(test_compound):
    df = pd.read_excel("./web/test.xlsx")
    df['sub_similarity'] = [get_similarity_1(
        test_compound, df['substrate_smiles_canonical'][i]) for i in range(len(df))]
    df['similarity_pro'] = None
    df['react_product'] = None
    df['score'] = None
    for i in range(len(df)):
        template = df['Revised Templates'][i]
        try:
            rxn = rdChemReactions.ReactionFromSmarts(template)
            reacts = Chem.MolFromSmiles(test_compound)
            products = rxn.RunReactant(reacts, 0)
            df['react_product'][i] = Chem.MolToSmiles(products[0][0])
            df['similarity_pro'][i] = get_similarity_1(
                df['prod_smiles_canonical'][i], df['react_product'][i])
            score = (df['similarity_pro'][i]) * (df['sub_similarity'][i])
            df['score'][i] = score
        except:
            continue

    # 排序输出(希望能保留socre和结果一起输出）
    dfmap = {}

    df.sort_values(by=['score'], axis=0, ascending=False, inplace=True)
    df = df.reset_index(drop=True)
    top = []
    for j in range(len(df)):
        try:
            if df['score'][j] > 0:
                product = canonicalize_smiles(df['react_product'][j])
                try:
                    t = dfmap[product]
                except:
                    dfmap[product] = df['score'][j]
                top.append(product)
        except:
            continue
    top_2 = list(set(top))
    top_2.sort(key=top.index)
    print(top_2)
    return top_2,dfmap

def main(file_path, test_compound):
    # input希望是一个template文件，dataframe格式；和一个test compound，smile格式
    # 1.打开template文件
    df = pd.read_excel(file_path)
    df['sub_similarity'] = [get_similarity_1(
        test_compound, df['substrate_smiles_canonical'][i]) for i in range(len(df))]
    df['similarity_pro'] = None
    df['react_product'] = None
    df['score'] = None
    for i in range(len(df)):
        template = df['Revised Templates'][i]
        try:
            rxn = rdChemReactions.ReactionFromSmarts(template)
            reacts = Chem.MolFromSmiles(test_compound)
            products = rxn.RunReactant(reacts, 0)
            df['react_product'][i] = Chem.MolToSmiles(products[0][0])
            df['similarity_pro'][i] = get_similarity_1(
                df['prod_smiles_canonical'][i], df['react_product'][i])
            score = (df['similarity_pro'][i]) * (df['sub_similarity'][i])
            df['score'][i] = score
        except:
            continue

    # 排序输出(希望能保留socre和结果一起输出）
    dfmap = {}

    df.sort_values(by=['score'], axis=0, ascending=False, inplace=True)
    df = df.reset_index(drop=True)
    top = []
    for j in range(len(df)):
        try:
            if df['score'][j] > 0:
                product = canonicalize_smiles(df['react_product'][j])
                try:
                    t = dfmap[product]
                except:
                    dfmap[product] = df['score'][j]
                top.append(product)
        except:
            continue
    top_2 = list(set(top))
    top_2.sort(key=top.index)
    return top_2,dfmap


if __name__ == "__main__":
    forecast('C1=CC(=CC=C1NC(=O)NC2=CC(=C(C=C2)Cl)Cl)Cl')
    
    #parser = argparse.ArgumentParser(description='输入结构，获取与库中近似结构')
    #parser.add_argument("-p", "--path", required=True, help="Excel文件名")
    #parser.add_argument("-c", "--test_compound", required=True,
    #                    help="测试结构,例如('C1=CC(=CC=C1NC(=O)NC2=CC(=C(C=C2)Cl)Cl)Cl')")
    #args = parser.parse_args()
    #main(args.path, args.test_compound)
    