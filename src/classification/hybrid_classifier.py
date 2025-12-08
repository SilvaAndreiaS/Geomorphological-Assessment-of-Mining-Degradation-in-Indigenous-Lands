"""
Classificador Híbrido combinando métodos tradicionais e Machine Learning
para detecção de cicatrizes de garimpo
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import xgboost as xgb


class SpectralIndices:
    """Classe para cálculo de índices espectrais"""
    
    @staticmethod
    def calculate_ndvi(nir: np.ndarray, red: np.ndarray) -> np.ndarray:
        """
        Calcula NDVI (Normalized Difference Vegetation Index)
        NDVI = (NIR - Red) / (NIR + Red)
        
        Args:
            nir: Banda do infravermelho próximo
            red: Banda do vermelho
            
        Returns:
            Array com valores de NDVI
        """
        with np.errstate(divide='ignore', invalid='ignore'):
            ndvi = (nir - red) / (nir + red)
            ndvi = np.nan_to_num(ndvi, nan=0.0)
        return ndvi
    
    @staticmethod
    def calculate_ndwi(green: np.ndarray, nir: np.ndarray) -> np.ndarray:
        """
        Calcula NDWI (Normalized Difference Water Index)
        NDWI = (Green - NIR) / (Green + NIR)
        
        Args:
            green: Banda verde
            nir: Banda do infravermelho próximo
            
        Returns:
            Array com valores de NDWI
        """
        with np.errstate(divide='ignore', invalid='ignore'):
            ndwi = (green - nir) / (green + nir)
            ndwi = np.nan_to_num(ndwi, nan=0.0)
        return ndwi
    
    @staticmethod
    def calculate_ndmi(nir: np.ndarray, swir: np.ndarray) -> np.ndarray:
        """
        Calcula NDMI (Normalized Difference Mining Index)
        NDMI = (SWIR - NIR) / (SWIR + NIR)
        
        Args:
            nir: Banda do infravermelho próximo
            swir: Banda do infravermelho de ondas curtas
            
        Returns:
            Array com valores de NDMI
        """
        with np.errstate(divide='ignore', invalid='ignore'):
            ndmi = (swir - nir) / (swir + nir)
            ndmi = np.nan_to_num(ndmi, nan=0.0)
        return ndmi
    
    @staticmethod
    def calculate_bsi(blue: np.ndarray, red: np.ndarray, 
                      nir: np.ndarray, swir: np.ndarray) -> np.ndarray:
        """
        Calcula BSI (Bare Soil Index)
        BSI = ((SWIR + Red) - (NIR + Blue)) / ((SWIR + Red) + (NIR + Blue))
        
        Args:
            blue: Banda azul
            red: Banda vermelha
            nir: Banda do infravermelho próximo
            swir: Banda do infravermelho de ondas curtas
            
        Returns:
            Array com valores de BSI
        """
        with np.errstate(divide='ignore', invalid='ignore'):
            numerator = (swir + red) - (nir + blue)
            denominator = (swir + red) + (nir + blue)
            bsi = numerator / denominator
            bsi = np.nan_to_num(bsi, nan=0.0)
        return bsi


class TraditionalClassifier:
    """Métodos tradicionais de classificação"""
    
    def __init__(self, config: Dict):
        """
        Inicializa classificador tradicional
        
        Args:
            config: Configuração do projeto
        """
        self.config = config
        self.scaler = StandardScaler()
    
    def kmeans_clustering(
        self, 
        data: np.ndarray, 
        n_clusters: int = 10
    ) -> np.ndarray:
        """
        Classificação não supervisionada usando K-means
        
        Args:
            data: Array de features (shape: [n_samples, n_features])
            n_clusters: Número de clusters
            
        Returns:
            Array de labels
        """
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(data)
        return labels
    
    def maximum_likelihood_classification(
        self, 
        data: np.ndarray, 
        training_data: np.ndarray,
        training_labels: np.ndarray
    ) -> np.ndarray:
        """
        Classificação supervisionada por máxima verossimilhança
        (Implementada como Gaussian Naive Bayes)
        
        Args:
            data: Dados a classificar
            training_data: Dados de treinamento
            training_labels: Labels de treinamento
            
        Returns:
            Array de labels preditos
        """
        from sklearn.naive_bayes import GaussianNB
        
        clf = GaussianNB()
        clf.fit(training_data, training_labels)
        predictions = clf.predict(data)
        return predictions
    
    def spectral_angle_mapping(
        self, 
        data: np.ndarray, 
        reference_spectra: Dict[str, np.ndarray]
    ) -> np.ndarray:
        """
        Classificação por Spectral Angle Mapper (SAM)
        
        Args:
            data: Array de dados espectrais
            reference_spectra: Dicionário com espectros de referência por classe
            
        Returns:
            Array de labels
        """
        # Reshape data se necessário
        original_shape = data.shape
        if len(data.shape) == 3:
            data_2d = data.reshape(data.shape[0], -1).T
        else:
            data_2d = data
        
        # Calcula ângulo espectral para cada classe
        class_names = list(reference_spectra.keys())
        angles = np.zeros((len(class_names), data_2d.shape[0]))
        
        for i, (class_name, ref_spectrum) in enumerate(reference_spectra.items()):
            # Calcula ângulo espectral
            dot_product = np.dot(data_2d, ref_spectrum)
            norm_data = np.linalg.norm(data_2d, axis=1)
            norm_ref = np.linalg.norm(ref_spectrum)
            
            with np.errstate(divide='ignore', invalid='ignore'):
                cos_angle = dot_product / (norm_data * norm_ref)
                cos_angle = np.clip(cos_angle, -1, 1)
                angles[i] = np.arccos(cos_angle)
        
        # Atribui classe com menor ângulo
        labels = np.argmin(angles, axis=0)
        
        if len(original_shape) == 3:
            labels = labels.reshape(original_shape[1], original_shape[2])
        
        return labels


class MachineLearningClassifier:
    """Classificadores de Machine Learning"""
    
    def __init__(self, config: Dict):
        """
        Inicializa classificador de ML
        
        Args:
            config: Configuração do projeto
        """
        self.config = config
        self.ml_config = config.get('classification', {}).get('hybrid_approach', {}).get('machine_learning', [])
        self.models = {}
        self.scaler = StandardScaler()
    
    def train_random_forest(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray,
        **kwargs
    ) -> RandomForestClassifier:
        """
        Treina classificador Random Forest
        
        Args:
            X_train: Dados de treinamento
            y_train: Labels de treinamento
            **kwargs: Parâmetros adicionais
            
        Returns:
            Modelo treinado
        """
        # Obtém parâmetros da configuração
        rf_config = next((c for c in self.ml_config if c.get('algorithm') == 'random_forest'), {})
        n_estimators = kwargs.get('n_estimators', rf_config.get('n_estimators', 100))
        max_depth = kwargs.get('max_depth', rf_config.get('max_depth', 20))
        
        clf = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42,
            n_jobs=-1
        )
        
        clf.fit(X_train, y_train)
        self.models['random_forest'] = clf
        return clf
    
    def train_xgboost(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray,
        **kwargs
    ) -> xgb.XGBClassifier:
        """
        Treina classificador XGBoost
        
        Args:
            X_train: Dados de treinamento
            y_train: Labels de treinamento
            **kwargs: Parâmetros adicionais
            
        Returns:
            Modelo treinado
        """
        # Obtém parâmetros da configuração
        xgb_config = next((c for c in self.ml_config if c.get('algorithm') == 'xgboost'), {})
        n_estimators = kwargs.get('n_estimators', xgb_config.get('n_estimators', 100))
        learning_rate = kwargs.get('learning_rate', xgb_config.get('learning_rate', 0.1))
        
        clf = xgb.XGBClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            random_state=42,
            n_jobs=-1
        )
        
        clf.fit(X_train, y_train)
        self.models['xgboost'] = clf
        return clf
    
    def train_svm(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray,
        **kwargs
    ) -> SVC:
        """
        Treina classificador SVM
        
        Args:
            X_train: Dados de treinamento
            y_train: Labels de treinamento
            **kwargs: Parâmetros adicionais
            
        Returns:
            Modelo treinado
        """
        # Obtém parâmetros da configuração
        svm_config = next((c for c in self.ml_config if c.get('algorithm') == 'svm'), {})
        kernel = kwargs.get('kernel', svm_config.get('kernel', 'rbf'))
        C = kwargs.get('C', svm_config.get('C', 1.0))
        
        # Normaliza dados para SVM
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        clf = SVC(kernel=kernel, C=C, random_state=42)
        clf.fit(X_train_scaled, y_train)
        self.models['svm'] = clf
        return clf
    
    def predict(
        self, 
        X: np.ndarray, 
        model_name: str = 'random_forest'
    ) -> np.ndarray:
        """
        Faz predições com modelo treinado
        
        Args:
            X: Dados para predição
            model_name: Nome do modelo a usar
            
        Returns:
            Predições
        """
        if model_name not in self.models:
            raise ValueError(f"Modelo '{model_name}' não foi treinado")
        
        model = self.models[model_name]
        
        # Normaliza se for SVM
        if model_name == 'svm':
            X = self.scaler.transform(X)
        
        return model.predict(X)


class HybridClassifier:
    """Classificador Híbrido combinando métodos tradicionais e ML"""
    
    def __init__(self, config: Dict):
        """
        Inicializa classificador híbrido
        
        Args:
            config: Configuração do projeto
        """
        self.config = config
        self.classification_config = config.get('classification', {})
        self.traditional_classifier = TraditionalClassifier(config)
        self.ml_classifier = MachineLearningClassifier(config)
        self.spectral_indices = SpectralIndices()
    
    def extract_features(
        self, 
        data: np.ndarray,
        band_mapping: Optional[Dict[str, int]] = None
    ) -> np.ndarray:
        """
        Extrai features espectrais da imagem
        
        Args:
            data: Array de dados (shape: [bands, height, width])
            band_mapping: Mapeamento de nomes de bandas para índices
            
        Returns:
            Array de features
        """
        features = []
        
        # Adiciona bandas originais
        for i in range(data.shape[0]):
            features.append(data[i].ravel())
        
        # Calcula índices espectrais se as bandas necessárias estiverem disponíveis
        if band_mapping is not None:
            if 'red' in band_mapping and 'nir' in band_mapping:
                ndvi = self.spectral_indices.calculate_ndvi(
                    data[band_mapping['nir']], 
                    data[band_mapping['red']]
                )
                features.append(ndvi.ravel())
            
            if 'green' in band_mapping and 'nir' in band_mapping:
                ndwi = self.spectral_indices.calculate_ndwi(
                    data[band_mapping['green']], 
                    data[band_mapping['nir']]
                )
                features.append(ndwi.ravel())
            
            if 'nir' in band_mapping and 'swir' in band_mapping:
                ndmi = self.spectral_indices.calculate_ndmi(
                    data[band_mapping['nir']], 
                    data[band_mapping['swir']]
                )
                features.append(ndmi.ravel())
            
            if all(k in band_mapping for k in ['blue', 'red', 'nir', 'swir']):
                bsi = self.spectral_indices.calculate_bsi(
                    data[band_mapping['blue']],
                    data[band_mapping['red']],
                    data[band_mapping['nir']],
                    data[band_mapping['swir']]
                )
                features.append(bsi.ravel())
        
        # Empilha features
        features_array = np.column_stack(features)
        return features_array
    
    def train_hybrid_model(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray
    ):
        """
        Treina modelos híbridos
        
        Args:
            X_train: Dados de treinamento
            y_train: Labels de treinamento
        """
        print("Treinando Random Forest...")
        self.ml_classifier.train_random_forest(X_train, y_train)
        
        print("Treinando XGBoost...")
        self.ml_classifier.train_xgboost(X_train, y_train)
        
        print("Treinando SVM...")
        self.ml_classifier.train_svm(X_train, y_train)
        
        print("Treinamento concluído!")
    
    def ensemble_prediction(
        self, 
        X: np.ndarray,
        method: str = 'voting',
        weights: Optional[List[float]] = None
    ) -> np.ndarray:
        """
        Faz predição ensemble combinando múltiplos modelos
        
        Args:
            X: Dados para predição
            method: Método de ensemble ('voting', 'weighted_average')
            weights: Pesos para cada modelo (opcional)
            
        Returns:
            Predições ensemble
        """
        predictions = []
        
        # Obtém predições de cada modelo
        for model_name in ['random_forest', 'xgboost', 'svm']:
            if model_name in self.ml_classifier.models:
                pred = self.ml_classifier.predict(X, model_name)
                predictions.append(pred)
        
        if not predictions:
            raise ValueError("Nenhum modelo foi treinado")
        
        predictions = np.array(predictions)
        
        if method == 'voting':
            # Votação majoritária
            from scipy import stats
            ensemble_pred = stats.mode(predictions, axis=0, keepdims=False)[0]
        elif method == 'weighted_average':
            # Média ponderada (requer probabilidades)
            if weights is None:
                weights = [1.0 / len(predictions)] * len(predictions)
            # Simplificação: usa votação ponderada
            ensemble_pred = np.average(predictions, axis=0, weights=weights).round().astype(int)
        else:
            raise ValueError(f"Método desconhecido: {method}")
        
        return ensemble_pred
    
    def classify(
        self, 
        data: np.ndarray,
        training_data: Optional[Tuple[np.ndarray, np.ndarray]] = None,
        band_mapping: Optional[Dict[str, int]] = None
    ) -> np.ndarray:
        """
        Classifica imagem usando abordagem híbrida
        
        Args:
            data: Imagem a classificar (shape: [bands, height, width])
            training_data: Tupla (X_train, y_train) opcional
            band_mapping: Mapeamento de bandas opcional
            
        Returns:
            Mapa de classificação
        """
        original_shape = data.shape[1:]
        
        # Extrai features
        print("Extraindo features...")
        features = self.extract_features(data, band_mapping)
        
        # Treina modelos se dados de treinamento forem fornecidos
        if training_data is not None:
            X_train, y_train = training_data
            self.train_hybrid_model(X_train, y_train)
        
        # Faz predição ensemble
        print("Classificando imagem...")
        classification = self.ensemble_prediction(features)
        
        # Reshape para dimensões originais
        classification = classification.reshape(original_shape)
        
        return classification
    
    def evaluate(
        self, 
        X_test: np.ndarray, 
        y_test: np.ndarray
    ) -> Dict:
        """
        Avalia desempenho dos modelos
        
        Args:
            X_test: Dados de teste
            y_test: Labels de teste
            
        Returns:
            Dicionário com métricas de avaliação
        """
        results = {}
        
        for model_name in ['random_forest', 'xgboost', 'svm']:
            if model_name in self.ml_classifier.models:
                y_pred = self.ml_classifier.predict(X_test, model_name)
                
                accuracy = accuracy_score(y_test, y_pred)
                conf_matrix = confusion_matrix(y_test, y_pred)
                class_report = classification_report(y_test, y_pred, output_dict=True)
                
                results[model_name] = {
                    'accuracy': accuracy,
                    'confusion_matrix': conf_matrix,
                    'classification_report': class_report
                }
        
        # Avalia ensemble
        y_pred_ensemble = self.ensemble_prediction(X_test)
        results['ensemble'] = {
            'accuracy': accuracy_score(y_test, y_pred_ensemble),
            'confusion_matrix': confusion_matrix(y_test, y_pred_ensemble),
            'classification_report': classification_report(y_test, y_pred_ensemble, output_dict=True)
        }
        
        return results
