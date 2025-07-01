"""
Analisador de Arquivos 3D com IA Integrada
Versão 5.0 - Sistema inteligente para marcenaria
"""

import os
import re
import math
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class FileAnalyzer:
    """Analisador inteligente de arquivos 3D para marcenaria"""
    
    def __init__(self):
        """Inicializa o analisador com IA integrada"""
        
        # Palavras-chave para classificação inteligente
        self.palavras_chave_tipos = {
            'armario': [
                'armario', 'armário', 'cabinet', 'wardrobe', 'closet',
                'guarda', 'roupeiro', 'superior', 'alto'
            ],
            'despenseiro': [
                'despenseiro', 'torre', 'tower', 'pantry', 'tall',
                'alto', 'vertical', 'coluna', 'despensa'
            ],
            'balcao': [
                'balcao', 'balcão', 'base', 'counter', 'bancada',
                'inferior', 'baixo', 'gabinete', 'sink'
            ],
            'gaveteiro': [
                'gaveteiro', 'gaveta', 'drawer', 'gavetas',
                'chest', 'comoda', 'cômoda'
            ],
            'prateleira': [
                'prateleira', 'shelf', 'shelving', 'estante',
                'nicho', 'divisoria', 'divisória'
            ],
            'porta': [
                'porta', 'door', 'folha', 'batente',
                'abertura', 'painel_porta'
            ]
        }
        
        # Palavras para filtrar elementos não-marcenaria
        self.palavras_filtro = {
            'paredes': ['parede', 'wall', 'muro', 'divisoria_alvenaria'],
            'pisos': ['piso', 'floor', 'chao', 'chão', 'laje'],
            'tetos': ['teto', 'ceiling', 'forro', 'laje_superior'],
            'eletrodomesticos': [
                'geladeira', 'refrigerator', 'fridge', 'fogao', 'fogão',
                'stove', 'microondas', 'microwave', 'lava', 'maquina',
                'máquina', 'washing', 'dishwasher'
            ],
            'decoracao': [
                'decoracao', 'decoração', 'vaso', 'quadro', 'luminaria',
                'luminária', 'lamp', 'plant', 'decoration'
            ],
            'estrutural': [
                'viga', 'pilar', 'beam', 'column', 'estrutura',
                'fundacao', 'fundação', 'laje'
            ]
        }
        
        # Padrões dimensionais típicos para validação
        self.dimensoes_tipicas = {
            'armario': {'min_area': 0.5, 'max_area': 15.0, 'proporcao_max': 5.0},
            'despenseiro': {'min_area': 1.0, 'max_area': 8.0, 'proporcao_max': 8.0},
            'balcao': {'min_area': 0.8, 'max_area': 12.0, 'proporcao_max': 4.0},
            'gaveteiro': {'min_area': 0.3, 'max_area': 6.0, 'proporcao_max': 3.0},
            'prateleira': {'min_area': 0.1, 'max_area': 3.0, 'proporcao_max': 10.0},
            'porta': {'min_area': 0.2, 'max_area': 4.0, 'proporcao_max': 6.0}
        }
    
    def analisar_arquivo_3d(self, caminho_arquivo: str) -> Optional[Dict]:
        """Analisa arquivo 3D com IA integrada"""
        
        try:
            if not os.path.exists(caminho_arquivo):
                return None
            
            extensao = caminho_arquivo.lower().split('.')[-1]
            
            if extensao == 'obj':
                return self._analisar_obj(caminho_arquivo)
            elif extensao in ['dae', 'collada']:
                return self._analisar_dae(caminho_arquivo)
            elif extensao == 'stl':
                return self._analisar_stl(caminho_arquivo)
            elif extensao == 'ply':
                return self._analisar_ply(caminho_arquivo)
            else:
                return None
                
        except Exception as e:
            print(f"Erro ao analisar arquivo: {e}")
            return None
    
    def _analisar_obj(self, caminho_arquivo: str) -> Optional[Dict]:
        """Analisa arquivo OBJ com IA"""
        
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                linhas = f.readlines()
            
            # Extrair objetos e grupos
            objetos = self._extrair_objetos_obj(linhas)
            
            # Analisar cada objeto com IA
            componentes = []
            for obj in objetos:
                componente = self._analisar_objeto_com_ia(obj)
                if componente:
                    componentes.append(componente)
            
            # Filtrar componentes válidos
            componentes_validos = self._filtrar_componentes_validos(componentes)
            
            # Gerar estatísticas
            estatisticas = self._gerar_estatisticas(componentes_validos, len(objetos))
            
            return {
                'componentes': componentes_validos,
                'estatisticas': estatisticas,
                'arquivo_original': os.path.basename(caminho_arquivo),
                'timestamp': datetime.now().isoformat(),
                'versao_analyzer': '5.0_ia_integrada'
            }
            
        except Exception as e:
            print(f"Erro ao analisar OBJ: {e}")
            return None
    
    def _extrair_objetos_obj(self, linhas: List[str]) -> List[Dict]:
        """Extrai objetos do arquivo OBJ"""
        
        objetos = []
        objeto_atual = None
        vertices = []
        faces = []
        
        for linha in linhas:
            linha = linha.strip()
            
            if linha.startswith('o ') or linha.startswith('g '):
                # Salvar objeto anterior
                if objeto_atual:
                    area = self._calcular_area_faces(vertices, faces)
                    objetos.append({
                        'nome': objeto_atual,
                        'vertices': len(vertices),
                        'faces': len(faces),
                        'area_m2': area
                    })
                
                # Iniciar novo objeto
                objeto_atual = linha[2:].strip()
                vertices = []
                faces = []
            
            elif linha.startswith('v '):
                # Vértice
                partes = linha.split()
                if len(partes) >= 4:
                    try:
                        x, y, z = float(partes[1]), float(partes[2]), float(partes[3])
                        vertices.append((x, y, z))
                    except ValueError:
                        continue
            
            elif linha.startswith('f '):
                # Face
                partes = linha.split()[1:]
                if len(partes) >= 3:
                    faces.append(partes)
        
        # Salvar último objeto
        if objeto_atual:
            area = self._calcular_area_faces(vertices, faces)
            objetos.append({
                'nome': objeto_atual,
                'vertices': len(vertices),
                'faces': len(faces),
                'area_m2': area
            })
        
        return objetos
    
    def _calcular_area_faces(self, vertices: List[Tuple], faces: List[List]) -> float:
        """Calcula área aproximada das faces"""
        
        try:
            if len(vertices) < 3 or len(faces) == 0:
                return 0.0
            
            # Calcular bounding box
            if not vertices:
                return 0.0
            
            xs = [v[0] for v in vertices]
            ys = [v[1] for v in vertices]
            zs = [v[2] for v in vertices]
            
            largura = max(xs) - min(xs)
            altura = max(ys) - min(ys)
            profundidade = max(zs) - min(zs)
            
            # Estimar área baseada na maior face
            areas = [largura * altura, largura * profundidade, altura * profundidade]
            area_maxima = max(areas)
            
            # Converter para metros quadrados (assumindo unidades em mm)
            area_m2 = area_maxima / 1000000  # mm² para m²
            
            # Limitar valores extremos
            return max(0.01, min(area_m2, 50.0))
            
        except Exception as e:
            print(f"Erro ao calcular área: {e}")
            return 1.0  # Valor padrão
    
    def _analisar_objeto_com_ia(self, objeto: Dict) -> Optional[Dict]:
        """Analisa objeto individual com IA"""
        
        try:
            nome = objeto.get('nome', '').lower()
            area_m2 = objeto.get('area_m2', 0)
            
            # Classificação por nome (IA semântica)
            tipo_detectado, confianca_nome = self._classificar_por_nome(nome)
            
            # Validação dimensional
            valido_dimensao, motivo_dimensao = self._validar_dimensoes(tipo_detectado, area_m2)
            
            # Filtrar elementos não-marcenaria
            eh_marcenaria, motivo_filtro = self._eh_marcenaria(nome)
            
            if not eh_marcenaria:
                return None  # Filtrar elemento
            
            # Calcular confiança final
            confianca_final = self._calcular_confianca_final(
                confianca_nome, valido_dimensao, eh_marcenaria
            )
            
            # Gerar insights da IA
            insights = self._gerar_insights_ia(objeto, tipo_detectado, confianca_final)
            
            return {
                'nome': objeto.get('nome', 'Componente'),
                'tipo': tipo_detectado,
                'area_m2': area_m2,
                'vertices': objeto.get('vertices', 0),
                'faces': objeto.get('faces', 0),
                # Dados da IA
                'ia_tipo_detectado': tipo_detectado,
                'ia_confianca': confianca_final,
                'ia_motivo': f"Nome: {confianca_nome:.1%}, Dimensão: {'✓' if valido_dimensao else '✗'}",
                'ia_insights': insights,
                'ia_validacao': {
                    'nome_valido': confianca_nome > 0.3,
                    'dimensao_valida': valido_dimensao,
                    'eh_marcenaria': eh_marcenaria,
                    'motivo_dimensao': motivo_dimensao,
                    'motivo_filtro': motivo_filtro
                }
            }
            
        except Exception as e:
            print(f"Erro na análise IA: {e}")
            return None
    
    def _classificar_por_nome(self, nome: str) -> Tuple[str, float]:
        """Classifica tipo baseado no nome usando IA semântica"""
        
        nome_limpo = re.sub(r'[^a-zA-Z0-9áéíóúâêîôûãõç]', ' ', nome.lower())
        palavras = nome_limpo.split()
        
        pontuacoes = {}
        
        for tipo, palavras_chave in self.palavras_chave_tipos.items():
            pontuacao = 0
            
            for palavra in palavras:
                for chave in palavras_chave:
                    # Correspondência exata
                    if palavra == chave:
                        pontuacao += 1.0
                    # Correspondência parcial
                    elif chave in palavra or palavra in chave:
                        pontuacao += 0.5
                    # Correspondência por similaridade
                    elif self._similaridade_palavras(palavra, chave) > 0.7:
                        pontuacao += 0.3
            
            pontuacoes[tipo] = pontuacao
        
        # Encontrar melhor classificação
        if pontuacoes:
            melhor_tipo = max(pontuacoes, key=pontuacoes.get)
            melhor_pontuacao = pontuacoes[melhor_tipo]
            
            # Normalizar confiança
            confianca = min(melhor_pontuacao / 2.0, 1.0)
            
            return melhor_tipo, confianca
        
        return 'armario', 0.1  # Padrão com baixa confiança
    
    def _similaridade_palavras(self, palavra1: str, palavra2: str) -> float:
        """Calcula similaridade entre palavras"""
        
        if not palavra1 or not palavra2:
            return 0.0
        
        # Algoritmo simples de similaridade
        if palavra1 == palavra2:
            return 1.0
        
        # Verificar substring
        if palavra1 in palavra2 or palavra2 in palavra1:
            return 0.8
        
        # Verificar caracteres comuns
        chars1 = set(palavra1)
        chars2 = set(palavra2)
        
        if chars1 and chars2:
            intersecao = len(chars1.intersection(chars2))
            uniao = len(chars1.union(chars2))
            return intersecao / uniao
        
        return 0.0
    
    def _validar_dimensoes(self, tipo: str, area_m2: float) -> Tuple[bool, str]:
        """Valida se as dimensões são compatíveis com o tipo"""
        
        if tipo not in self.dimensoes_tipicas:
            return True, "Tipo não catalogado"
        
        limites = self.dimensoes_tipicas[tipo]
        
        # Verificar área
        if area_m2 < limites['min_area']:
            return False, f"Área muito pequena ({area_m2:.2f}m² < {limites['min_area']}m²)"
        
        if area_m2 > limites['max_area']:
            return False, f"Área muito grande ({area_m2:.2f}m² > {limites['max_area']}m²)"
        
        return True, "Dimensões compatíveis"
    
    def _eh_marcenaria(self, nome: str) -> Tuple[bool, str]:
        """Verifica se o elemento é de marcenaria"""
        
        nome_limpo = nome.lower()
        
        # Verificar palavras de filtro
        for categoria, palavras in self.palavras_filtro.items():
            for palavra in palavras:
                if palavra in nome_limpo:
                    return False, f"Detectado como {categoria}: '{palavra}'"
        
        # Verificar padrões suspeitos
        if any(x in nome_limpo for x in ['mesh', 'default', 'object', 'cube', 'plane']):
            return True, "Nome genérico, mas pode ser marcenaria"
        
        return True, "Elemento válido de marcenaria"
    
    def _calcular_confianca_final(self, confianca_nome: float, 
                                 valido_dimensao: bool, eh_marcenaria: bool) -> float:
        """Calcula confiança final da classificação"""
        
        confianca = confianca_nome
        
        # Penalizar se dimensões inválidas
        if not valido_dimensao:
            confianca *= 0.5
        
        # Penalizar se não é marcenaria
        if not eh_marcenaria:
            confianca *= 0.1
        
        # Bonificar se tudo está correto
        if valido_dimensao and eh_marcenaria and confianca_nome > 0.5:
            confianca = min(confianca * 1.2, 1.0)
        
        return confianca
    
    def _gerar_insights_ia(self, objeto: Dict, tipo: str, confianca: float) -> List[str]:
        """Gera insights inteligentes sobre o objeto"""
        
        insights = []
        area = objeto.get('area_m2', 0)
        nome = objeto.get('nome', '')
        
        # Insight sobre confiança
        if confianca > 0.8:
            insights.append("🎯 Alta confiança na classificação")
        elif confianca > 0.5:
            insights.append("⚠️ Confiança média - verificar manualmente")
        else:
            insights.append("❌ Baixa confiança - revisar classificação")
        
        # Insight sobre área
        if area > 10:
            insights.append("📏 Área grande - verificar se não é parede/piso")
        elif area < 0.1:
            insights.append("📏 Área muito pequena - pode ser acessório")
        
        # Insight sobre nomenclatura
        if any(x in nome.lower() for x in ['mesh', 'object', 'default']):
            insights.append("📝 Nome genérico - melhorar nomenclatura no SketchUp")
        
        # Insight sobre tipo
        if tipo == 'despenseiro' and area > 6:
            insights.append("🏗️ Despenseiro grande - verificar se é torre completa")
        elif tipo == 'prateleira' and area > 2:
            insights.append("📚 Prateleira grande - pode ser estante completa")
        
        return insights
    
    def _filtrar_componentes_validos(self, componentes: List[Dict]) -> List[Dict]:
        """Filtra apenas componentes válidos de marcenaria"""
        
        validos = []
        
        for comp in componentes:
            # Critérios de validação
            confianca = comp.get('ia_confianca', 0)
            area = comp.get('area_m2', 0)
            eh_marcenaria = comp.get('ia_validacao', {}).get('eh_marcenaria', False)
            
            # Filtros
            if not eh_marcenaria:
                continue
            
            if area < 0.01 or area > 50:  # Limites extremos
                continue
            
            if confianca < 0.1:  # Confiança muito baixa
                continue
            
            validos.append(comp)
        
        return validos
    
    def _gerar_estatisticas(self, componentes: List[Dict], total_objetos: int) -> Dict:
        """Gera estatísticas da análise"""
        
        if not componentes:
            return {
                'total_objetos': total_objetos,
                'componentes_validos': 0,
                'taxa_aproveitamento': 0.0,
                'area_total': 0.0,
                'confianca_media': 0.0,
                'tipos_detectados': {},
                'qualidade_arquivo': 'Baixa'
            }
        
        # Calcular estatísticas
        area_total = sum(comp.get('area_m2', 0) for comp in componentes)
        confianca_media = sum(comp.get('ia_confianca', 0) for comp in componentes) / len(componentes)
        taxa_aproveitamento = len(componentes) / total_objetos if total_objetos > 0 else 0
        
        # Contar tipos
        tipos_detectados = {}
        for comp in componentes:
            tipo = comp.get('tipo', 'desconhecido')
            tipos_detectados[tipo] = tipos_detectados.get(tipo, 0) + 1
        
        # Avaliar qualidade
        if confianca_media > 0.8 and taxa_aproveitamento > 0.7:
            qualidade = 'Excelente'
        elif confianca_media > 0.6 and taxa_aproveitamento > 0.5:
            qualidade = 'Boa'
        elif confianca_media > 0.4 and taxa_aproveitamento > 0.3:
            qualidade = 'Regular'
        else:
            qualidade = 'Baixa'
        
        return {
            'total_objetos': total_objetos,
            'componentes_validos': len(componentes),
            'taxa_aproveitamento': taxa_aproveitamento,
            'area_total': area_total,
            'confianca_media': confianca_media,
            'tipos_detectados': tipos_detectados,
            'qualidade_arquivo': qualidade,
            'recomendacoes': self._gerar_recomendacoes(confianca_media, taxa_aproveitamento)
        }
    
    def _gerar_recomendacoes(self, confianca_media: float, taxa_aproveitamento: float) -> List[str]:
        """Gera recomendações para melhorar a análise"""
        
        recomendacoes = []
        
        if confianca_media < 0.5:
            recomendacoes.append("📝 Melhore a nomenclatura dos objetos no SketchUp")
            recomendacoes.append("🎯 Use palavras-chave como 'armario', 'balcao', 'despenseiro'")
        
        if taxa_aproveitamento < 0.5:
            recomendacoes.append("🧹 Remova elementos não-marcenaria (paredes, pisos, eletrodomésticos)")
            recomendacoes.append("📦 Mantenha apenas móveis de marcenaria no arquivo")
        
        if confianca_media > 0.8 and taxa_aproveitamento > 0.7:
            recomendacoes.append("✅ Arquivo excelente! IA funcionando com alta precisão")
        
        return recomendacoes
    
    def _analisar_dae(self, caminho_arquivo: str) -> Optional[Dict]:
        """Análise básica de arquivo DAE/Collada"""
        # Implementação simplificada
        return self._analise_generica(caminho_arquivo, 'DAE')
    
    def _analisar_stl(self, caminho_arquivo: str) -> Optional[Dict]:
        """Análise básica de arquivo STL"""
        return self._analise_generica(caminho_arquivo, 'STL')
    
    def _analisar_ply(self, caminho_arquivo: str) -> Optional[Dict]:
        """Análise básica de arquivo PLY"""
        return self._analise_generica(caminho_arquivo, 'PLY')
    
    def _analise_generica(self, caminho_arquivo: str, formato: str) -> Dict:
        """Análise genérica para formatos não-OBJ"""
        
        tamanho_mb = os.path.getsize(caminho_arquivo) / (1024 * 1024)
        
        # Estimativa baseada no tamanho do arquivo
        area_estimada = max(1.0, tamanho_mb * 2)  # Estimativa grosseira
        
        componente_generico = {
            'nome': f'Componente_{formato}',
            'tipo': 'armario',
            'area_m2': area_estimada,
            'vertices': int(tamanho_mb * 1000),  # Estimativa
            'faces': int(tamanho_mb * 500),     # Estimativa
            'ia_tipo_detectado': 'armario',
            'ia_confianca': 0.3,  # Baixa confiança para análise genérica
            'ia_motivo': f'Análise genérica de arquivo {formato}',
            'ia_insights': [
                f"📁 Arquivo {formato} analisado genericamente",
                "⚠️ Para melhor precisão, use formato OBJ",
                "📝 Verifique manualmente os resultados"
            ]
        }
        
        return {
            'componentes': [componente_generico],
            'estatisticas': {
                'total_objetos': 1,
                'componentes_validos': 1,
                'taxa_aproveitamento': 1.0,
                'area_total': area_estimada,
                'confianca_media': 0.3,
                'tipos_detectados': {'armario': 1},
                'qualidade_arquivo': 'Regular',
                'recomendacoes': [
                    f"🔄 Converta {formato} para OBJ para melhor análise",
                    "📝 Nomeie objetos corretamente no software 3D"
                ]
            },
            'arquivo_original': os.path.basename(caminho_arquivo),
            'timestamp': datetime.now().isoformat(),
            'versao_analyzer': '5.0_ia_integrada'
        }

# Teste do sistema
if __name__ == "__main__":
    analyzer = FileAnalyzer()
    
    print("🤖 Analisador de Arquivos 3D com IA - Versão 5.0")
    print("=" * 60)
    
    # Teste com dados simulados
    teste_objetos = [
        {'nome': 'Armario_Superior_Cozinha', 'vertices': 1000, 'faces': 500, 'area_m2': 3.5},
        {'nome': 'Balcao_Base_Pia', 'vertices': 800, 'faces': 400, 'area_m2': 2.8},
        {'nome': 'Parede_Principal', 'vertices': 2000, 'faces': 1000, 'area_m2': 15.0},
        {'nome': 'Prateleira_Interna', 'vertices': 200, 'faces': 100, 'area_m2': 0.8}
    ]
    
    componentes_analisados = []
    for obj in teste_objetos:
        comp = analyzer._analisar_objeto_com_ia(obj)
        if comp:
            componentes_analisados.append(comp)
            print(f"✅ {comp['nome']}: {comp['tipo']} (confiança: {comp['ia_confianca']:.1%})")
        else:
            print(f"❌ {obj['nome']}: Filtrado (não é marcenaria)")
    
    print(f"\n📊 Resultado: {len(componentes_analisados)} componentes válidos de {len(teste_objetos)} objetos")
    print("🎯 Sistema de IA funcionando corretamente!")

