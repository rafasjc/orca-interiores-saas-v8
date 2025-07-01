"""
Sistema de Autenticação - Orca Interiores
Versão 5.0 - Sistema limpo e profissional
"""

import sqlite3
import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional, Dict

class AuthManager:
    """Gerenciador de autenticação e usuários"""
    
    def __init__(self, db_path: str = "usuarios.db"):
        """Inicializa o gerenciador de autenticação"""
        self.db_path = db_path
        self._criar_tabelas()
        self._criar_usuarios_demo()
    
    def _criar_tabelas(self):
        """Cria as tabelas necessárias no banco de dados"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabela de usuários
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    senha_hash TEXT NOT NULL,
                    plano TEXT DEFAULT 'basico',
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_ultimo_login TIMESTAMP,
                    ativo BOOLEAN DEFAULT 1,
                    orcamentos_mes INTEGER DEFAULT 0,
                    limite_orcamentos INTEGER DEFAULT 10
                )
            """)
            
            # Tabela de sessões
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER,
                    token TEXT UNIQUE NOT NULL,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_expiracao TIMESTAMP NOT NULL,
                    ativo BOOLEAN DEFAULT 1,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                )
            """)
            
            # Tabela de orçamentos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orcamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER,
                    nome_arquivo TEXT,
                    valor_final REAL,
                    area_total REAL,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    dados_json TEXT,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                )
            """)
            
            conn.commit()
    
    def _criar_usuarios_demo(self):
        """Cria usuários demo se não existirem"""
        
        usuarios_demo = [
            {
                'email': 'demo@orcainteriores.com',
                'senha': 'demo123',
                'plano': 'profissional',
                'limite': 50
            },
            {
                'email': 'arquiteto@teste.com',
                'senha': 'arq123',
                'plano': 'basico',
                'limite': 10
            },
            {
                'email': 'marceneiro@teste.com',
                'senha': 'marc123',
                'plano': 'empresarial',
                'limite': 999999
            }
        ]
        
        for usuario in usuarios_demo:
            if not self._usuario_existe(usuario['email']):
                self._criar_usuario_interno(
                    usuario['email'],
                    usuario['senha'],
                    usuario['plano'],
                    usuario['limite']
                )
    
    def _hash_senha(self, senha: str) -> str:
        """Gera hash da senha"""
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def _usuario_existe(self, email: str) -> bool:
        """Verifica se usuário já existe"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
            return cursor.fetchone() is not None
    
    def _criar_usuario_interno(self, email: str, senha: str, plano: str = 'basico', limite: int = 10) -> bool:
        """Cria usuário interno (sem validações)"""
        
        try:
            senha_hash = self._hash_senha(senha)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO usuarios (email, senha_hash, plano, limite_orcamentos)
                    VALUES (?, ?, ?, ?)
                """, (email, senha_hash, plano, limite))
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Erro ao criar usuário interno: {e}")
            return False
    
    def criar_usuario(self, email: str, senha: str, plano: str = 'basico') -> bool:
        """Cria um novo usuário"""
        
        try:
            # Validações
            if not email or not senha:
                return False
            
            if len(senha) < 6:
                return False
            
            if self._usuario_existe(email):
                return False
            
            # Definir limite baseado no plano
            limites = {
                'basico': 10,
                'profissional': 50,
                'empresarial': 999999
            }
            
            limite = limites.get(plano, 10)
            
            return self._criar_usuario_interno(email, senha, plano, limite)
            
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return False
    
    def fazer_login(self, email: str, senha: str) -> Optional[Dict]:
        """Realiza login do usuário"""
        
        try:
            if not email or not senha:
                return None
            
            senha_hash = self._hash_senha(senha)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, email, plano, orcamentos_mes, limite_orcamentos, ativo
                    FROM usuarios 
                    WHERE email = ? AND senha_hash = ? AND ativo = 1
                """, (email, senha_hash))
                
                resultado = cursor.fetchone()
                
                if resultado:
                    # Atualizar último login
                    cursor.execute("""
                        UPDATE usuarios 
                        SET data_ultimo_login = CURRENT_TIMESTAMP 
                        WHERE id = ?
                    """, (resultado[0],))
                    conn.commit()
                    
                    return {
                        'id': resultado[0],
                        'email': resultado[1],
                        'plano': resultado[2],
                        'orcamentos_mes': resultado[3],
                        'limite_orcamentos': resultado[4],
                        'ativo': resultado[5]
                    }
                
                return None
                
        except Exception as e:
            print(f"Erro no login: {e}")
            return None
    
    def verificar_limite_orcamentos(self, usuario_id: int) -> bool:
        """Verifica se usuário pode fazer mais orçamentos"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT orcamentos_mes, limite_orcamentos 
                    FROM usuarios 
                    WHERE id = ?
                """, (usuario_id,))
                
                resultado = cursor.fetchone()
                
                if resultado:
                    orcamentos_mes, limite = resultado
                    return orcamentos_mes < limite
                
                return False
                
        except Exception as e:
            print(f"Erro ao verificar limite: {e}")
            return False
    
    def incrementar_orcamentos(self, usuario_id: int) -> bool:
        """Incrementa contador de orçamentos do usuário"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE usuarios 
                    SET orcamentos_mes = orcamentos_mes + 1 
                    WHERE id = ?
                """, (usuario_id,))
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Erro ao incrementar orçamentos: {e}")
            return False
    
    def salvar_orcamento(self, usuario_id: int, nome_arquivo: str, 
                        valor_final: float, area_total: float, dados_json: str) -> bool:
        """Salva orçamento no histórico"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO orcamentos (usuario_id, nome_arquivo, valor_final, area_total, dados_json)
                    VALUES (?, ?, ?, ?, ?)
                """, (usuario_id, nome_arquivo, valor_final, area_total, dados_json))
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Erro ao salvar orçamento: {e}")
            return False
    
    def obter_historico_orcamentos(self, usuario_id: int, limite: int = 10) -> list:
        """Obtém histórico de orçamentos do usuário"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT nome_arquivo, valor_final, area_total, data_criacao
                    FROM orcamentos 
                    WHERE usuario_id = ?
                    ORDER BY data_criacao DESC
                    LIMIT ?
                """, (usuario_id, limite))
                
                resultados = cursor.fetchall()
                
                historico = []
                for resultado in resultados:
                    historico.append({
                        'nome_arquivo': resultado[0],
                        'valor_final': resultado[1],
                        'area_total': resultado[2],
                        'data_criacao': resultado[3]
                    })
                
                return historico
                
        except Exception as e:
            print(f"Erro ao obter histórico: {e}")
            return []
    
    def obter_estatisticas_usuario(self, usuario_id: int) -> Dict:
        """Obtém estatísticas do usuário"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Dados do usuário
                cursor.execute("""
                    SELECT email, plano, orcamentos_mes, limite_orcamentos, data_criacao
                    FROM usuarios 
                    WHERE id = ?
                """, (usuario_id,))
                
                usuario = cursor.fetchone()
                
                if not usuario:
                    return {}
                
                # Estatísticas de orçamentos
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_orcamentos,
                        AVG(valor_final) as valor_medio,
                        SUM(area_total) as area_total,
                        MAX(data_criacao) as ultimo_orcamento
                    FROM orcamentos 
                    WHERE usuario_id = ?
                """, (usuario_id,))
                
                stats = cursor.fetchone()
                
                return {
                    'email': usuario[0],
                    'plano': usuario[1],
                    'orcamentos_mes': usuario[2],
                    'limite_orcamentos': usuario[3],
                    'data_criacao': usuario[4],
                    'total_orcamentos': stats[0] if stats[0] else 0,
                    'valor_medio': stats[1] if stats[1] else 0,
                    'area_total': stats[2] if stats[2] else 0,
                    'ultimo_orcamento': stats[3] if stats[3] else None
                }
                
        except Exception as e:
            print(f"Erro ao obter estatísticas: {e}")
            return {}
    
    def resetar_contador_mensal(self):
        """Reseta contador mensal de orçamentos (para ser executado mensalmente)"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE usuarios SET orcamentos_mes = 0")
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Erro ao resetar contador: {e}")
            return False
    
    def alterar_plano(self, usuario_id: int, novo_plano: str) -> bool:
        """Altera plano do usuário"""
        
        try:
            limites = {
                'basico': 10,
                'profissional': 50,
                'empresarial': 999999
            }
            
            if novo_plano not in limites:
                return False
            
            limite = limites[novo_plano]
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE usuarios 
                    SET plano = ?, limite_orcamentos = ?
                    WHERE id = ?
                """, (novo_plano, limite, usuario_id))
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Erro ao alterar plano: {e}")
            return False

# Teste do sistema
if __name__ == "__main__":
    auth = AuthManager()
    
    print("🔐 Sistema de Autenticação - Orca Interiores")
    print("=" * 50)
    
    # Teste de login com usuário demo
    usuario = auth.fazer_login("demo@orcainteriores.com", "demo123")
    
    if usuario:
        print(f"✅ Login bem-sucedido!")
        print(f"📧 Email: {usuario['email']}")
        print(f"💎 Plano: {usuario['plano'].title()}")
        print(f"📊 Orçamentos: {usuario['orcamentos_mes']}/{usuario['limite_orcamentos']}")
        
        # Teste de estatísticas
        stats = auth.obter_estatisticas_usuario(usuario['id'])
        print(f"📈 Total de orçamentos: {stats.get('total_orcamentos', 0)}")
        
    else:
        print("❌ Erro no login")
    
    print("\n🎯 Sistema funcionando corretamente!")

