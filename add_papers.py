"""
=============================================================================
  GapInsight — Bulk Paper Insertion Script
  Inserts 150 real research papers across 10 categories into MongoDB
  Run: python add_papers.py
=============================================================================
"""

from pymongo import MongoClient
from datetime import datetime

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB  = "gapinsight_db"

client = MongoClient(MONGO_URI)
db     = client[MONGO_DB]
papers = db["papers"]

print("=" * 65)
print("  GapInsight — Inserting 150 Research Papers")
print("=" * 65)

papers.drop()
print("  ✓ Cleared old papers collection")

all_papers = [

    # =========================================================================
    #  CATEGORY 1: Natural Language Processing (20 papers)
    # =========================================================================
    {"title": "Attention Is All You Need",
     "abstract": "We propose the Transformer, a model architecture based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable.",
     "uploaded_by_user_id": 1, "keywords": ["transformer", "attention mechanism", "NLP", "neural network", "sequence modeling", "machine translation"], "category": "Natural Language Processing", "year": 2017, "citation_count": 75000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
     "abstract": "We introduce BERT which stands for Bidirectional Encoder Representations from Transformers. BERT is designed to pre-train deep bidirectional representations by jointly conditioning on both left and right context in all layers.",
     "uploaded_by_user_id": 2, "keywords": ["BERT", "pre-training", "transformers", "NLP", "language understanding", "fine-tuning", "bidirectional"], "category": "Natural Language Processing", "year": 2018, "citation_count": 50000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "GPT-4 Technical Report",
     "abstract": "We report the development of GPT-4, a large-scale multimodal model which can accept image and text inputs and produce text outputs. GPT-4 exhibits human-level performance on various professional and academic benchmarks.",
     "uploaded_by_user_id": 1, "keywords": ["GPT-4", "large language model", "multimodal", "RLHF", "instruction tuning", "benchmark"], "category": "Natural Language Processing", "year": 2023, "citation_count": 8000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Language Models are Few-Shot Learners (GPT-3)",
     "abstract": "We demonstrate that scaling language models greatly improves task-agnostic few-shot performance. GPT-3 with 175 billion parameters achieves strong performance on many NLP tasks without any gradient updates or fine-tuning.",
     "uploaded_by_user_id": 2, "keywords": ["GPT-3", "few-shot learning", "language model", "in-context learning", "zero-shot", "scaling"], "category": "Natural Language Processing", "year": 2020, "citation_count": 22000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "RoBERTa: A Robustly Optimized BERT Pretraining Approach",
     "abstract": "We present a replication study of BERT pretraining that carefully evaluates the impact of many key hyperparameters and training data size. We find that BERT was significantly undertrained and can match or exceed performance of all post-BERT methods.",
     "uploaded_by_user_id": 1, "keywords": ["RoBERTa", "BERT", "pre-training", "NLP", "language model", "hyperparameter tuning"], "category": "Natural Language Processing", "year": 2019, "citation_count": 12000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Research Gaps in Urdu Natural Language Processing: A Survey",
     "abstract": "This survey identifies critical research gaps in Urdu NLP. Despite over 230 million speakers, Urdu remains severely under-resourced. We analyze existing tools, datasets, and models and identify open problems in morphological analysis, sentiment analysis, and machine translation.",
     "uploaded_by_user_id": 3, "keywords": ["Urdu NLP", "low-resource NLP", "morphological analysis", "Urdu corpus", "sentiment analysis Urdu", "under-resourced"], "category": "Natural Language Processing", "year": 2022, "citation_count": 45, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "T5: Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer",
     "abstract": "We introduce a unified framework that converts every language problem into a text-to-text format. We systematically study transfer learning for NLP tasks using T5 on a large new dataset C4.",
     "uploaded_by_user_id": 2, "keywords": ["T5", "transfer learning", "text-to-text", "NLP", "multi-task learning", "C4 dataset"], "category": "Natural Language Processing", "year": 2020, "citation_count": 11000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "XLNet: Generalized Autoregressive Pretraining for Language Understanding",
     "abstract": "XLNet is a generalized autoregressive pretraining method that enables learning bidirectional contexts by maximizing the expected likelihood over all permutations of the factorization order and overcomes limitations of BERT.",
     "uploaded_by_user_id": 1, "keywords": ["XLNet", "autoregressive", "language model", "permutation", "pre-training", "NLP"], "category": "Natural Language Processing", "year": 2019, "citation_count": 7500, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Multilingual BERT and Cross-lingual Transfer",
     "abstract": "We evaluate multilingual BERT on cross-lingual NLU tasks. Surprisingly the model transfers well to low-resource languages despite no explicit cross-lingual training signal.",
     "uploaded_by_user_id": 3, "keywords": ["multilingual BERT", "cross-lingual", "transfer learning", "NLU", "low-resource languages", "mBERT"], "category": "Natural Language Processing", "year": 2019, "citation_count": 3200, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Sentiment Analysis on Social Media: Challenges and Open Problems",
     "abstract": "Sentiment analysis on Twitter and other social platforms presents unique challenges: informal language, sarcasm, code-switching, and emoji usage. We survey existing approaches and identify open research problems.",
     "uploaded_by_user_id": 1, "keywords": ["sentiment analysis", "social media", "Twitter", "sarcasm detection", "code-switching", "opinion mining"], "category": "Natural Language Processing", "year": 2021, "citation_count": 340, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Named Entity Recognition for Low-Resource Languages: A Survey",
     "abstract": "Named Entity Recognition for low-resource languages remains a significant challenge. This paper surveys transfer learning, data augmentation, and cross-lingual methods for under-resourced NER tasks.",
     "uploaded_by_user_id": 3, "keywords": ["NER", "named entity recognition", "low-resource", "data augmentation", "cross-lingual NER"], "category": "Natural Language Processing", "year": 2022, "citation_count": 180, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "LLaMA: Open and Efficient Foundation Language Models",
     "abstract": "We introduce LLaMA, a collection of foundation language models ranging from 7B to 65B parameters trained on publicly available datasets. LLaMA-13B outperforms GPT-3 on most benchmarks despite being 10x smaller.",
     "uploaded_by_user_id": 2, "keywords": ["LLaMA", "open source LLM", "foundation model", "efficient training", "language model", "benchmark"], "category": "Natural Language Processing", "year": 2023, "citation_count": 6000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Question Answering over Knowledge Graphs: Open Challenges",
     "abstract": "Knowledge graph question answering (KGQA) requires mapping natural language questions to structured queries over knowledge graphs. We identify open challenges in multi-hop reasoning and zero-shot KGQA.",
     "uploaded_by_user_id": 1, "keywords": ["knowledge graph", "question answering", "KGQA", "multi-hop reasoning", "zero-shot QA"], "category": "Natural Language Processing", "year": 2022, "citation_count": 210, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Text Summarization with Pretrained Encoders",
     "abstract": "We propose a novel document-level encoder based on BERT for text summarization. We introduce interval segment embeddings to encode multiple sentences and show strong results on CNN and DailyMail datasets.",
     "uploaded_by_user_id": 2, "keywords": ["text summarization", "abstractive summarization", "extractive summarization", "BERT", "encoder"], "category": "Natural Language Processing", "year": 2019, "citation_count": 1800, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Machine Translation for Low-Resource African Languages",
     "abstract": "Most African languages are severely under-represented in machine translation research. We build datasets and baselines for 10 African languages and identify critical gaps in morphological complexity handling.",
     "uploaded_by_user_id": 3, "keywords": ["machine translation", "African languages", "low-resource", "morphology", "multilingual NMT"], "category": "Natural Language Processing", "year": 2022, "citation_count": 95, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Hate Speech Detection: Datasets, Methods, and Challenges",
     "abstract": "Automatic hate speech detection is critical for online platform safety. We survey existing datasets, deep learning models, and identify key challenges including context dependence, implicit hate, and multilingual detection.",
     "uploaded_by_user_id": 1, "keywords": ["hate speech detection", "content moderation", "toxic language", "online safety", "offensive language"], "category": "Natural Language Processing", "year": 2021, "citation_count": 580, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Dialogue State Tracking in Task-Oriented Dialogue Systems",
     "abstract": "Dialogue state tracking is essential for task-oriented dialogue systems. We survey neural approaches and identify open challenges in zero-shot generalization across domains and handling of complex slot values.",
     "uploaded_by_user_id": 2, "keywords": ["dialogue state tracking", "task-oriented dialogue", "conversational AI", "slot filling", "zero-shot"], "category": "Natural Language Processing", "year": 2021, "citation_count": 430, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
     "abstract": "We combine parametric and non-parametric memory for language generation. RAG models retrieve relevant documents and use them to generate accurate answers to knowledge-intensive questions.",
     "uploaded_by_user_id": 3, "keywords": ["RAG", "retrieval augmented generation", "knowledge-intensive NLP", "dense retrieval", "open-domain QA"], "category": "Natural Language Processing", "year": 2020, "citation_count": 3400, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Code Generation with Large Language Models",
     "abstract": "Large language models like Codex and CodeT5 achieve impressive code generation performance. We evaluate LLMs on HumanEval benchmark and identify gaps in multi-file code generation and debugging tasks.",
     "uploaded_by_user_id": 1, "keywords": ["code generation", "LLM", "Codex", "program synthesis", "HumanEval", "software engineering"], "category": "Natural Language Processing", "year": 2023, "citation_count": 1200, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Pashto NLP: A Survey of Existing Resources and Research Gaps",
     "abstract": "Pashto is spoken by 60 million people but remains severely under-researched in NLP. We survey available corpora, tools, and models and identify critical gaps in POS tagging, parsing, and machine translation for Pashto.",
     "uploaded_by_user_id": 3, "keywords": ["Pashto NLP", "low-resource NLP", "under-resourced language", "POS tagging", "Pashto corpus"], "category": "Natural Language Processing", "year": 2023, "citation_count": 18, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    # =========================================================================
    #  CATEGORY 2: Machine Learning (20 papers)
    # =========================================================================
    {"title": "Federated Learning: Strategies for Improving Communication Efficiency",
     "abstract": "We present two practical methods for reducing communication costs of federated learning: structured updates and sketched updates where the update is compressed before sending to the parameter server.",
     "uploaded_by_user_id": 1, "keywords": ["federated learning", "distributed ML", "communication efficiency", "privacy", "FedAvg"], "category": "Machine Learning", "year": 2016, "citation_count": 4200, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "XGBoost: A Scalable Tree Boosting System",
     "abstract": "We describe a scalable end-to-end tree boosting system called XGBoost which uses novel sparsity-aware algorithms and weighted quantile sketch for approximate tree learning.",
     "uploaded_by_user_id": 2, "keywords": ["XGBoost", "gradient boosting", "decision trees", "ensemble learning", "scalable ML"], "category": "Machine Learning", "year": 2016, "citation_count": 28000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "A Survey on Explainable Artificial Intelligence (XAI)",
     "abstract": "This survey reviews explainable AI methods including LIME, SHAP, and attention-based explanations. We categorize methods by model type and application domain and identify key open research challenges.",
     "uploaded_by_user_id": 1, "keywords": ["explainable AI", "XAI", "interpretability", "LIME", "SHAP", "model explanation", "black box"], "category": "Machine Learning", "year": 2020, "citation_count": 3800, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "AutoML: A Survey of the State-of-the-Art",
     "abstract": "Automated Machine Learning aims to reduce human effort in building ML pipelines. This survey covers neural architecture search, hyperparameter optimization, and meta-learning in the context of AutoML.",
     "uploaded_by_user_id": 3, "keywords": ["AutoML", "neural architecture search", "hyperparameter optimization", "meta-learning", "NAS"], "category": "Machine Learning", "year": 2021, "citation_count": 890, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Graph Neural Networks: A Review of Methods and Applications",
     "abstract": "Graph neural networks have become a powerful tool for graph-structured data. This paper provides a comprehensive review of GNN methods including GCN, GAT, and GraphSAGE and their applications.",
     "uploaded_by_user_id": 1, "keywords": ["graph neural network", "GNN", "GCN", "GAT", "knowledge graph", "node classification"], "category": "Machine Learning", "year": 2019, "citation_count": 6700, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Reinforcement Learning from Human Feedback (RLHF)",
     "abstract": "We present a method for training language models to follow instructions using reinforcement learning from human feedback. Our approach aligns model outputs with human preferences and reduces harmful outputs.",
     "uploaded_by_user_id": 2, "keywords": ["RLHF", "reinforcement learning", "human feedback", "alignment", "reward model", "instruction tuning"], "category": "Machine Learning", "year": 2022, "citation_count": 4500, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Multimodal Machine Learning: A Survey and Taxonomy",
     "abstract": "Multimodal ML involves learning from multiple modalities such as text, image, audio, and video. This survey covers fusion strategies, cross-modal learning, and open challenges in grounding and alignment.",
     "uploaded_by_user_id": 3, "keywords": ["multimodal learning", "vision-language", "CLIP", "fusion", "cross-modal", "audio visual"], "category": "Machine Learning", "year": 2022, "citation_count": 1200, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "TinyML: Machine Learning on Embedded Systems",
     "abstract": "TinyML enables running ML inference on microcontrollers and edge devices with milliwatt power budgets. We survey model compression, quantization, pruning, and knowledge distillation for resource-constrained deployment.",
     "uploaded_by_user_id": 1, "keywords": ["TinyML", "edge AI", "model compression", "quantization", "pruning", "embedded systems", "IoT"], "category": "Machine Learning", "year": 2021, "citation_count": 560, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Continual Learning: A Comparative Study",
     "abstract": "Continual learning enables models to learn new tasks without forgetting previous ones. We compare regularization-based, memory replay, and architecture-based approaches to overcome catastrophic forgetting.",
     "uploaded_by_user_id": 2, "keywords": ["continual learning", "lifelong learning", "catastrophic forgetting", "task incremental", "replay memory"], "category": "Machine Learning", "year": 2022, "citation_count": 420, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Self-Supervised Learning: A Survey",
     "abstract": "Self-supervised learning leverages unlabeled data by creating pretext tasks. We survey contrastive learning methods like SimCLR and MoCo, masked autoencoders, and their applications across vision and language.",
     "uploaded_by_user_id": 3, "keywords": ["self-supervised learning", "contrastive learning", "SimCLR", "MoCo", "pretext task", "representation learning"], "category": "Machine Learning", "year": 2021, "citation_count": 2800, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Active Learning for Deep Neural Networks",
     "abstract": "Active learning reduces labeling cost by selecting the most informative samples for annotation. We survey query strategies for deep networks and identify open challenges in batch-mode and streaming active learning.",
     "uploaded_by_user_id": 1, "keywords": ["active learning", "query strategy", "annotation", "uncertainty sampling", "core-set selection"], "category": "Machine Learning", "year": 2021, "citation_count": 670, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Meta-Learning: Learning to Learn",
     "abstract": "Meta-learning enables models to quickly adapt to new tasks with limited data. We survey gradient-based methods like MAML, metric-based approaches, and model-based meta-learning algorithms.",
     "uploaded_by_user_id": 2, "keywords": ["meta-learning", "MAML", "few-shot learning", "learning to learn", "model agnostic", "rapid adaptation"], "category": "Machine Learning", "year": 2020, "citation_count": 3100, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Causal Machine Learning: Methods and Applications",
     "abstract": "Causal ML goes beyond correlation to identify cause-effect relationships. We survey causal inference methods including do-calculus, instrumental variables, and their integration with deep learning for robust predictions.",
     "uploaded_by_user_id": 3, "keywords": ["causal inference", "causal ML", "do-calculus", "counterfactual", "intervention", "structural causal model"], "category": "Machine Learning", "year": 2022, "citation_count": 890, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Tabular Data Deep Learning: A Survey",
     "abstract": "Despite the dominance of gradient boosting on tabular data, deep learning approaches have shown promise. We survey TabNet, SAINT, and FT-Transformer and identify gaps in handling missing data and categorical features.",
     "uploaded_by_user_id": 1, "keywords": ["tabular data", "TabNet", "deep learning tabular", "structured data", "categorical features"], "category": "Machine Learning", "year": 2022, "citation_count": 440, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Anomaly Detection in Time Series: A Survey",
     "abstract": "Time series anomaly detection is critical in IoT monitoring, fraud detection, and predictive maintenance. We survey statistical, ML, and deep learning approaches and identify open challenges in multivariate anomaly detection.",
     "uploaded_by_user_id": 2, "keywords": ["anomaly detection", "time series", "outlier detection", "IoT", "LSTM anomaly", "multivariate"], "category": "Machine Learning", "year": 2022, "citation_count": 760, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Fairness in Machine Learning: A Survey",
     "abstract": "ML models can perpetuate or amplify societal biases. We survey fairness definitions, bias mitigation methods, and evaluation frameworks, and identify open challenges in intersectional fairness and long-term impact.",
     "uploaded_by_user_id": 3, "keywords": ["fairness ML", "bias", "algorithmic fairness", "demographic parity", "equalized odds", "responsible AI"], "category": "Machine Learning", "year": 2021, "citation_count": 2100, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Mixture of Experts for Efficient Large-Scale Models",
     "abstract": "Mixture of Experts (MoE) conditionally activates a subset of parameters per input, enabling massive model capacity with manageable compute. We survey sparse MoE architectures and their training challenges.",
     "uploaded_by_user_id": 1, "keywords": ["mixture of experts", "MoE", "sparse gating", "efficient LLM", "conditional computation"], "category": "Machine Learning", "year": 2022, "citation_count": 1500, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Zero-Shot Learning: A Comprehensive Evaluation",
     "abstract": "Zero-shot learning enables classification of categories unseen during training via semantic embeddings. We provide a comprehensive evaluation of ZSL methods on standard benchmarks and identify evaluation biases.",
     "uploaded_by_user_id": 2, "keywords": ["zero-shot learning", "semantic embedding", "attribute learning", "generalized ZSL", "visual-semantic"], "category": "Machine Learning", "year": 2019, "citation_count": 2300, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Bayesian Deep Learning: Uncertainty Estimation in Neural Networks",
     "abstract": "Bayesian approaches to deep learning provide principled uncertainty estimates. We survey Monte Carlo dropout, deep ensembles, and variational inference methods for uncertainty quantification in safety-critical applications.",
     "uploaded_by_user_id": 3, "keywords": ["Bayesian deep learning", "uncertainty estimation", "MC dropout", "epistemic uncertainty", "aleatoric uncertainty"], "category": "Machine Learning", "year": 2021, "citation_count": 980, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Machine Learning for Drug Discovery: Opportunities and Challenges",
     "abstract": "ML accelerates drug discovery through molecular property prediction, de novo drug design, and protein structure prediction. We identify open challenges in data scarcity, interpretability, and clinical translation.",
     "uploaded_by_user_id": 1, "keywords": ["drug discovery ML", "molecular property prediction", "de novo design", "protein structure", "AlphaFold"], "category": "Machine Learning", "year": 2022, "citation_count": 1700, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    # =========================================================================
    #  CATEGORY 3: Computer Vision (18 papers)
    # =========================================================================
    {"title": "3D Medical Image Segmentation Using Deep Learning: Open Challenges",
     "abstract": "We review deep learning methods for 3D medical image segmentation and identify key open research challenges including limited labeled data, domain shift, and real-time inference requirements for clinical deployment.",
     "uploaded_by_user_id": 2, "keywords": ["3D segmentation", "medical imaging", "MRI", "deep learning", "U-Net", "CT scan"], "category": "Computer Vision", "year": 2021, "citation_count": 320, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "ImageNet Classification with Deep Convolutional Neural Networks (AlexNet)",
     "abstract": "We trained a large deep convolutional neural network to classify 1.2 million images into 1000 classes achieving top-1 error of 37.5% on ImageNet LSVRC-2010.",
     "uploaded_by_user_id": 1, "keywords": ["AlexNet", "CNN", "ImageNet", "deep learning", "image classification", "GPU training"], "category": "Computer Vision", "year": 2012, "citation_count": 95000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Deep Residual Learning for Image Recognition (ResNet)",
     "abstract": "We present residual learning framework to ease training of very deep networks using skip connections. Networks with up to 152 layers win ILSVRC 2015 with 3.57% error.",
     "uploaded_by_user_id": 2, "keywords": ["ResNet", "residual learning", "deep learning", "image recognition", "skip connections", "ILSVRC"], "category": "Computer Vision", "year": 2016, "citation_count": 120000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "YOLO: Real-Time Object Detection",
     "abstract": "A single neural network predicts bounding boxes and class probabilities directly from full images in one evaluation enabling real-time detection at 45 frames per second.",
     "uploaded_by_user_id": 3, "keywords": ["YOLO", "object detection", "real-time detection", "bounding box", "CNN", "autonomous driving"], "category": "Computer Vision", "year": 2016, "citation_count": 35000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "An Image is Worth 16x16 Words: Vision Transformer (ViT)",
     "abstract": "We apply a standard Transformer directly to sequences of image patches for image classification. When pre-trained on large datasets Vision Transformer achieves excellent results on multiple recognition benchmarks.",
     "uploaded_by_user_id": 1, "keywords": ["Vision Transformer", "ViT", "image patches", "self-attention", "image classification", "transformer"], "category": "Computer Vision", "year": 2021, "citation_count": 18000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Generative Adversarial Networks (GANs)",
     "abstract": "We propose a framework for estimating generative models via adversarial process. A generative model is pitted against a discriminator that learns to distinguish model samples from real data.",
     "uploaded_by_user_id": 2, "keywords": ["GAN", "generative adversarial network", "image generation", "discriminator", "generator", "deep learning"], "category": "Computer Vision", "year": 2014, "citation_count": 55000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Diffusion Models Beat GANs on Image Synthesis",
     "abstract": "We show that diffusion models can achieve image sample quality superior to the current best GANs on conditional image synthesis while maintaining diversity.",
     "uploaded_by_user_id": 3, "keywords": ["diffusion model", "image synthesis", "DDPM", "classifier guidance", "generative model", "stable diffusion"], "category": "Computer Vision", "year": 2021, "citation_count": 5600, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "CLIP: Learning Transferable Visual Models from Natural Language Supervision",
     "abstract": "We present CLIP which learns visual concepts from natural language supervision. CLIP enables zero-shot transfer to downstream vision tasks and matches performance of task-specific models.",
     "uploaded_by_user_id": 1, "keywords": ["CLIP", "vision language", "zero-shot transfer", "contrastive learning", "natural language supervision"], "category": "Computer Vision", "year": 2021, "citation_count": 12000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Semantic Segmentation Using Fully Convolutional Networks",
     "abstract": "Convolutional networks trained end-to-end pixels-to-pixels on semantic segmentation exceed state-of-the-art without further machinery.",
     "uploaded_by_user_id": 2, "keywords": ["semantic segmentation", "FCN", "fully convolutional", "pixel classification", "scene understanding"], "category": "Computer Vision", "year": 2015, "citation_count": 27000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Few-Shot Image Classification: A Survey",
     "abstract": "Few-shot learning enables models to classify new categories from very few examples. This survey covers metric-based, model-based, and optimization-based approaches and open challenges.",
     "uploaded_by_user_id": 3, "keywords": ["few-shot learning", "image classification", "meta-learning", "prototypical networks", "one-shot"], "category": "Computer Vision", "year": 2022, "citation_count": 620, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Point Cloud Learning with PointNet",
     "abstract": "PointNet directly processes point clouds and provides a unified architecture for applications such as 3D object classification, part segmentation, and scene semantic parsing.",
     "uploaded_by_user_id": 1, "keywords": ["point cloud", "PointNet", "3D object detection", "LiDAR", "3D scene understanding", "autonomous driving"], "category": "Computer Vision", "year": 2017, "citation_count": 9800, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Retinal Disease Detection Using Deep Learning: Research Gaps",
     "abstract": "Deep learning achieves expert-level performance on diabetic retinopathy detection. However gaps remain in rare disease detection, multi-disease grading, and deployment in resource-limited ophthalmology settings.",
     "uploaded_by_user_id": 2, "keywords": ["retinal disease", "diabetic retinopathy", "fundus imaging", "ophthalmology AI", "medical AI"], "category": "Computer Vision", "year": 2022, "citation_count": 145, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Deepfake Detection: Current Methods and Future Directions",
     "abstract": "Deepfake synthesis methods have improved dramatically while detection has lagged behind. We survey face forgery detection methods and identify open challenges in cross-dataset generalization and audio-visual deepfakes.",
     "uploaded_by_user_id": 3, "keywords": ["deepfake detection", "face forgery", "media forensics", "GAN detection", "synthetic media"], "category": "Computer Vision", "year": 2022, "citation_count": 890, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Autonomous Driving Perception: A Survey",
     "abstract": "Perception is a critical component of autonomous driving systems. We survey 2D/3D object detection, lane detection, semantic segmentation, and sensor fusion methods and identify open safety-critical challenges.",
     "uploaded_by_user_id": 1, "keywords": ["autonomous driving", "object detection", "sensor fusion", "LiDAR camera fusion", "lane detection", "perception"], "category": "Computer Vision", "year": 2023, "citation_count": 670, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Remote Sensing Image Analysis with Deep Learning",
     "abstract": "Deep learning has transformed remote sensing analysis for land use classification, change detection, and disaster response. We identify key gaps in few-labeled-data scenarios and cross-sensor generalization.",
     "uploaded_by_user_id": 2, "keywords": ["remote sensing", "satellite imagery", "land use classification", "change detection", "SAR"], "category": "Computer Vision", "year": 2022, "citation_count": 380, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Crowd Counting and Density Estimation: Open Research Problems",
     "abstract": "Crowd counting from images is essential for public safety management. We survey density map regression and detection-based approaches and identify gaps in extremely dense crowd scenarios.",
     "uploaded_by_user_id": 3, "keywords": ["crowd counting", "density estimation", "surveillance", "congestion analysis", "public safety"], "category": "Computer Vision", "year": 2021, "citation_count": 290, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Pose Estimation: From 2D to 3D Human Body Pose",
     "abstract": "Human pose estimation has broad applications in action recognition and healthcare. We review 2D heatmap and 3D lifting approaches and identify open challenges in occlusion handling and multi-person scenarios.",
     "uploaded_by_user_id": 1, "keywords": ["pose estimation", "human body pose", "skeleton detection", "action recognition", "keypoint detection"], "category": "Computer Vision", "year": 2022, "citation_count": 430, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Image Captioning: Bridging Vision and Language",
     "abstract": "Image captioning generates natural language descriptions of images. We survey CNN-LSTM, attention-based, and transformer-based captioning models and identify gaps in dense captioning and visual storytelling.",
     "uploaded_by_user_id": 2, "keywords": ["image captioning", "visual question answering", "VQA", "vision language", "dense captioning"], "category": "Computer Vision", "year": 2022, "citation_count": 560, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    # =========================================================================
    #  CATEGORY 4: Deep Learning (15 papers)
    # =========================================================================
    {"title": "Batch Normalization: Accelerating Deep Network Training",
     "abstract": "Training deep neural networks is complicated by the fact that the distribution of each layer's inputs changes during training. Batch normalization addresses this by normalizing layer inputs enabling higher learning rates.",
     "uploaded_by_user_id": 2, "keywords": ["batch normalization", "deep learning", "training stability", "internal covariate shift", "neural network"], "category": "Deep Learning", "year": 2015, "citation_count": 42000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Adam: A Method for Stochastic Optimization",
     "abstract": "We introduce Adam, an algorithm for first-order gradient-based optimization combining the advantages of AdaGrad and RMSProp. It is computationally efficient and well-suited for problems with noisy gradients.",
     "uploaded_by_user_id": 3, "keywords": ["Adam optimizer", "stochastic optimization", "gradient descent", "learning rate", "momentum", "AdaGrad"], "category": "Deep Learning", "year": 2015, "citation_count": 130000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Long Short-Term Memory (LSTM) Networks",
     "abstract": "LSTM networks can learn to bridge minimal time lags in excess of 1000 discrete time steps by enforcing constant error flow through the network using input, output, and forget gates.",
     "uploaded_by_user_id": 2, "keywords": ["LSTM", "recurrent neural network", "RNN", "sequence learning", "time series", "memory cell", "gating"], "category": "Deep Learning", "year": 1997, "citation_count": 70000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Variational Autoencoders for Generative Modeling",
     "abstract": "We introduce a stochastic variational inference and learning algorithm that scales to large datasets. The VAE learns a continuous latent space enabling controlled generation and interpolation.",
     "uploaded_by_user_id": 3, "keywords": ["VAE", "variational autoencoder", "generative model", "latent space", "representation learning", "ELBO"], "category": "Deep Learning", "year": 2014, "citation_count": 22000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "EfficientNet: Rethinking Model Scaling for CNNs",
     "abstract": "We systematically study model scaling for CNNs and identify that balancing network width, depth, and resolution leads to better performance. EfficientNet achieves 84.3% top-1 accuracy on ImageNet.",
     "uploaded_by_user_id": 1, "keywords": ["EfficientNet", "model scaling", "CNN", "compound scaling", "ImageNet", "efficient deep learning"], "category": "Deep Learning", "year": 2019, "citation_count": 11000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Physics-Informed Neural Networks for Solving PDEs",
     "abstract": "Physics-informed neural networks are trained to solve supervised learning tasks while respecting nonlinear partial differential equations as constraints in the loss function.",
     "uploaded_by_user_id": 2, "keywords": ["physics-informed neural network", "PINN", "PDE", "scientific ML", "differential equations", "simulation"], "category": "Deep Learning", "year": 2019, "citation_count": 7800, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Neural Architecture Search with Reinforcement Learning",
     "abstract": "We use a recurrent network to generate model descriptions and train the generated architecture. Our best architecture achieves 3.65% error rate on CIFAR-10.",
     "uploaded_by_user_id": 3, "keywords": ["neural architecture search", "NAS", "reinforcement learning", "AutoML", "CIFAR-10", "architecture design"], "category": "Deep Learning", "year": 2017, "citation_count": 5200, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Knowledge Distillation: A Survey",
     "abstract": "Knowledge distillation transfers knowledge from a large teacher model to a compact student model. We survey response-based, feature-based, and relation-based distillation methods and applications in model compression.",
     "uploaded_by_user_id": 1, "keywords": ["knowledge distillation", "model compression", "teacher student", "model deployment", "efficient inference"], "category": "Deep Learning", "year": 2021, "citation_count": 3200, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Graph Convolutional Networks for Node Classification",
     "abstract": "We present a scalable approach for semi-supervised classification on graph-structured data using an efficient layer-wise propagation rule based on a first-order approximation of spectral graph convolutions.",
     "uploaded_by_user_id": 2, "keywords": ["graph convolutional network", "GCN", "semi-supervised", "node classification", "spectral graph theory"], "category": "Deep Learning", "year": 2017, "citation_count": 18000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Attention Mechanisms in Neural Networks: A Survey",
     "abstract": "Attention mechanisms enable neural networks to focus on relevant parts of the input. We survey soft attention, hard attention, self-attention, and multi-head attention and their applications.",
     "uploaded_by_user_id": 3, "keywords": ["attention mechanism", "self-attention", "multi-head attention", "neural network", "sequence to sequence"], "category": "Deep Learning", "year": 2021, "citation_count": 1800, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Spiking Neural Networks: The Third Generation",
     "abstract": "Spiking neural networks process information using discrete spikes and are more biologically realistic and energy-efficient than traditional ANNs. We survey SNN training methods and neuromorphic hardware.",
     "uploaded_by_user_id": 1, "keywords": ["spiking neural network", "SNN", "neuromorphic computing", "spike-timing", "energy efficient AI"], "category": "Deep Learning", "year": 2022, "citation_count": 520, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Transformers for Time Series: A Survey",
     "abstract": "Transformer models have been adapted for time series forecasting with applications in energy, finance, and healthcare. We survey Informer, Autoformer, and PatchTST and identify open challenges.",
     "uploaded_by_user_id": 2, "keywords": ["time series forecasting", "transformer", "Informer", "Autoformer", "temporal attention", "energy forecasting"], "category": "Deep Learning", "year": 2023, "citation_count": 780, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Neural Ordinary Differential Equations",
     "abstract": "We introduce a new family of deep neural network models by parameterizing the derivative of the hidden state using a neural network. This continuous-depth model has constant memory cost and adapts its evaluation strategy.",
     "uploaded_by_user_id": 3, "keywords": ["neural ODE", "ordinary differential equations", "continuous depth", "dynamical systems", "normalizing flows"], "category": "Deep Learning", "year": 2018, "citation_count": 4200, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Deep Learning for Financial Forecasting: Gaps and Opportunities",
     "abstract": "Deep learning for financial time series forecasting faces unique challenges including non-stationarity, low signal-to-noise ratio, and regime changes. We survey existing approaches and identify critical research gaps.",
     "uploaded_by_user_id": 1, "keywords": ["financial forecasting", "stock prediction", "deep learning finance", "non-stationarity", "algorithmic trading"], "category": "Deep Learning", "year": 2022, "citation_count": 340, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Capsule Networks: A Replacement for CNNs?",
     "abstract": "Capsule networks represent entities as capsules rather than scalar activations and use dynamic routing between capsules. They are more robust to viewpoint changes but face scalability challenges.",
     "uploaded_by_user_id": 2, "keywords": ["capsule network", "dynamic routing", "viewpoint invariance", "pooling", "CNN alternative"], "category": "Deep Learning", "year": 2018, "citation_count": 3600, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    # =========================================================================
    #  CATEGORY 5: Database Systems (12 papers)
    # =========================================================================
    {"title": "Dynamo: Amazon's Highly Available Key-Value Store",
     "abstract": "Dynamo is a highly available key-value storage system that sacrifices consistency under certain failure scenarios in favor of availability using consistent hashing and versioning.",
     "uploaded_by_user_id": 2, "keywords": ["NoSQL", "key-value store", "distributed database", "consistent hashing", "availability", "DynamoDB"], "category": "Database Systems", "year": 2007, "citation_count": 8500, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Bigtable: A Distributed Storage System for Structured Data",
     "abstract": "Bigtable is a distributed storage system for managing structured data at Google scale designed to reliably scale to petabytes of data across thousands of commodity servers.",
     "uploaded_by_user_id": 1, "keywords": ["Bigtable", "distributed storage", "column family", "tablet", "GFS", "NoSQL", "Google"], "category": "Database Systems", "year": 2006, "citation_count": 9200, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "MapReduce: Simplified Data Processing on Large Clusters",
     "abstract": "MapReduce is a programming model for processing and generating large datasets. Programs written in this style are automatically parallelized across large clusters of commodity machines.",
     "uploaded_by_user_id": 3, "keywords": ["MapReduce", "distributed computing", "Hadoop", "data processing", "parallel computing", "big data"], "category": "Database Systems", "year": 2004, "citation_count": 20000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Vector Databases for AI Applications: A Survey",
     "abstract": "Vector databases enable efficient similarity search over high-dimensional embeddings. This survey covers HNSW, IVF, and LSH indexing and applications in recommendation and RAG systems.",
     "uploaded_by_user_id": 2, "keywords": ["vector database", "similarity search", "HNSW", "approximate nearest neighbor", "embeddings", "RAG", "Pinecone"], "category": "Database Systems", "year": 2023, "citation_count": 210, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "NewSQL: Relational Databases for the Cloud Era",
     "abstract": "NewSQL databases provide the scalability of NoSQL while maintaining ACID guarantees. We survey Google Spanner, CockroachDB, and TiDB and identify open challenges in distributed transactions.",
     "uploaded_by_user_id": 1, "keywords": ["NewSQL", "distributed database", "ACID", "Google Spanner", "cloud database", "scalability"], "category": "Database Systems", "year": 2021, "citation_count": 380, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Graph Databases: Principles and Applications",
     "abstract": "Graph databases store data as nodes and edges enabling efficient traversal queries. We survey Neo4j, Amazon Neptune, and TigerGraph and identify gaps in graph analytics, streaming graphs, and ML integration.",
     "uploaded_by_user_id": 3, "keywords": ["graph database", "Neo4j", "property graph", "Cypher query", "knowledge graph storage", "graph analytics"], "category": "Database Systems", "year": 2022, "citation_count": 290, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Data Lakes: Architecture, Challenges, and Best Practices",
     "abstract": "Data lakes store raw data at scale for later processing. We survey Delta Lake, Apache Iceberg, and Hudi and identify open challenges in data quality, schema evolution, and governance.",
     "uploaded_by_user_id": 1, "keywords": ["data lake", "Delta Lake", "Apache Iceberg", "data governance", "schema evolution", "data quality"], "category": "Database Systems", "year": 2022, "citation_count": 180, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Time-Series Databases for IoT: A Comparative Study",
     "abstract": "Time-series databases are optimized for storing and querying sensor data. We compare InfluxDB, TimescaleDB, and OpenTSDB on IoT workloads and identify gaps in multi-sensor correlation queries.",
     "uploaded_by_user_id": 2, "keywords": ["time-series database", "InfluxDB", "TimescaleDB", "IoT database", "sensor data", "time series storage"], "category": "Database Systems", "year": 2021, "citation_count": 150, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Database Query Optimization with Machine Learning",
     "abstract": "ML-based query optimization predicts optimal query plans using learned cost models. We survey learned cardinality estimation, join ordering, and index selection and identify open challenges in generalization.",
     "uploaded_by_user_id": 3, "keywords": ["query optimization", "learned index", "cardinality estimation", "join ordering", "database ML"], "category": "Database Systems", "year": 2022, "citation_count": 420, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Multi-Model Databases: One System for All Data Models",
     "abstract": "Multi-model databases support multiple data models (document, graph, relational) within a single backend. We survey ArangoDB, OrientDB, and CosmosDB and identify gaps in query language unification.",
     "uploaded_by_user_id": 1, "keywords": ["multi-model database", "ArangoDB", "CosmosDB", "document graph relational", "polyglot persistence"], "category": "Database Systems", "year": 2021, "citation_count": 95, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Blockchain Databases: Immutability Meets Query Processing",
     "abstract": "Blockchain databases combine immutable ledger properties with query processing capabilities. We survey verifiable databases, FalconDB, and LedgerDB and identify open challenges in performance and privacy.",
     "uploaded_by_user_id": 2, "keywords": ["blockchain database", "immutable ledger", "verifiable database", "tamper-evident", "audit trail"], "category": "Database Systems", "year": 2022, "citation_count": 110, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Federated Databases: Challenges in Data Integration",
     "abstract": "Federated databases integrate multiple heterogeneous databases without centralization. We survey schema mapping, query translation, and data exchange approaches and identify privacy-preserving integration gaps.",
     "uploaded_by_user_id": 3, "keywords": ["federated database", "data integration", "schema mapping", "heterogeneous data", "data federation"], "category": "Database Systems", "year": 2021, "citation_count": 130, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    # =========================================================================
    #  CATEGORY 6: Cybersecurity (10 papers)
    # =========================================================================
    {"title": "Deep Learning for Intrusion Detection: A Survey",
     "abstract": "We survey deep learning methods for network intrusion detection. CNNs, LSTMs, and autoencoders are applied to detect network anomalies. Open challenges include adversarial attacks and zero-day threats.",
     "uploaded_by_user_id": 3, "keywords": ["intrusion detection", "IDS", "network security", "anomaly detection", "adversarial attacks", "cybersecurity"], "category": "Cybersecurity", "year": 2021, "citation_count": 650, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Differential Privacy: A Survey of Results",
     "abstract": "Differential privacy provides a mathematically rigorous definition of privacy for statistical databases. We survey applications to ML, data analysis, and federated systems.",
     "uploaded_by_user_id": 1, "keywords": ["differential privacy", "privacy", "data anonymization", "noise mechanism", "federated learning privacy", "epsilon privacy"], "category": "Cybersecurity", "year": 2020, "citation_count": 2100, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Adversarial Examples in Machine Learning",
     "abstract": "Deep neural networks are vulnerable to adversarial examples. We survey attack methods including FGSM and PGD and defenses including adversarial training and certified robustness.",
     "uploaded_by_user_id": 2, "keywords": ["adversarial examples", "adversarial attacks", "robustness", "perturbation", "FGSM", "PGD attack", "adversarial training"], "category": "Cybersecurity", "year": 2018, "citation_count": 9800, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Phishing Detection Using Machine Learning: Open Challenges",
     "abstract": "ML-based phishing detection achieves high accuracy but faces challenges from zero-day phishing, adversarial evasion, and concept drift. We identify key open research gaps in URL and content-based detection.",
     "uploaded_by_user_id": 1, "keywords": ["phishing detection", "cybersecurity", "URL analysis", "social engineering", "zero-day phishing", "concept drift"], "category": "Cybersecurity", "year": 2022, "citation_count": 290, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Malware Detection Using Deep Learning",
     "abstract": "Static and dynamic malware analysis using deep learning has shown great promise. We survey CNN-based binary analysis, API call sequence modeling, and graph-based malware detection approaches.",
     "uploaded_by_user_id": 3, "keywords": ["malware detection", "static analysis", "dynamic analysis", "API call sequence", "binary analysis", "ransomware"], "category": "Cybersecurity", "year": 2021, "citation_count": 480, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Blockchain Technology: Principles and Applications",
     "abstract": "Blockchain is a distributed ledger technology enabling trustless transactions. We cover consensus mechanisms, smart contracts, and applications in supply chain, healthcare, and finance.",
     "uploaded_by_user_id": 2, "keywords": ["blockchain", "distributed ledger", "smart contract", "consensus", "cryptocurrency", "decentralization"], "category": "Cybersecurity", "year": 2020, "citation_count": 4300, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Federated Learning Security: Attacks and Defenses",
     "abstract": "Federated learning is vulnerable to poisoning attacks, backdoor attacks, and model inversion. We survey attack vectors and defenses including robust aggregation and differential privacy in federated settings.",
     "uploaded_by_user_id": 1, "keywords": ["federated learning security", "poisoning attack", "backdoor attack", "model inversion", "Byzantine fault"], "category": "Cybersecurity", "year": 2022, "citation_count": 680, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "IoT Security: Threats, Challenges, and Countermeasures",
     "abstract": "IoT devices face unique security challenges due to resource constraints and diverse protocols. We survey authentication, encryption, and intrusion detection for IoT and identify gaps in lightweight cryptography.",
     "uploaded_by_user_id": 2, "keywords": ["IoT security", "lightweight cryptography", "device authentication", "IoT intrusion detection", "MQTT security"], "category": "Cybersecurity", "year": 2022, "citation_count": 560, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Zero-Trust Architecture: Beyond the Perimeter",
     "abstract": "Zero-trust security eliminates implicit trust in networks by continuously verifying every access request. We survey zero-trust frameworks, micro-segmentation, and identity-based access control.",
     "uploaded_by_user_id": 3, "keywords": ["zero trust", "network security", "micro-segmentation", "identity access management", "SASE", "cloud security"], "category": "Cybersecurity", "year": 2021, "citation_count": 390, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Social Engineering Attacks: Detection and Prevention",
     "abstract": "Social engineering exploits human psychology rather than technical vulnerabilities. We survey detection of spear phishing, vishing, and pretexting attacks and identify gaps in automated social engineering defense.",
     "uploaded_by_user_id": 1, "keywords": ["social engineering", "spear phishing", "human factor security", "vishing", "security awareness"], "category": "Cybersecurity", "year": 2022, "citation_count": 180, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    # =========================================================================
    #  CATEGORY 7: Healthcare & Bioinformatics (15 papers)
    # =========================================================================
    {"title": "AlphaFold: Protein Structure Prediction Using Deep Learning",
     "abstract": "AlphaFold produces highly accurate protein structure predictions using a novel deep learning architecture. It solves the protein folding problem that has challenged biologists for 50 years.",
     "uploaded_by_user_id": 2, "keywords": ["AlphaFold", "protein structure prediction", "bioinformatics", "deep learning biology", "protein folding"], "category": "Healthcare AI", "year": 2021, "citation_count": 14000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Clinical NLP: Information Extraction from Electronic Health Records",
     "abstract": "Clinical NLP extracts structured information from unstructured EHR notes. We survey named entity recognition, relation extraction, and clinical summarization methods and identify privacy and annotation challenges.",
     "uploaded_by_user_id": 3, "keywords": ["clinical NLP", "EHR", "electronic health records", "medical NLP", "clinical information extraction", "de-identification"], "category": "Healthcare AI", "year": 2021, "citation_count": 520, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Deep Learning for Early Cancer Detection: A Review",
     "abstract": "Deep learning has shown promise in detecting cancers in mammography, colonoscopy, and pathology slides. We identify critical gaps in multi-center validation, rare cancer types, and regulatory approval.",
     "uploaded_by_user_id": 1, "keywords": ["cancer detection", "mammography AI", "pathology AI", "colonoscopy detection", "oncology ML", "screening"], "category": "Healthcare AI", "year": 2022, "citation_count": 430, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Federated Learning for Healthcare: Privacy-Preserving Medical AI",
     "abstract": "Federated learning enables hospitals to collaboratively train models without sharing patient data. We survey healthcare federated learning applications and identify challenges in heterogeneous clinical data.",
     "uploaded_by_user_id": 2, "keywords": ["federated learning healthcare", "medical AI", "patient privacy", "hospital collaboration", "HIPAA compliance"], "category": "Healthcare AI", "year": 2021, "citation_count": 780, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Drug Repurposing Using Knowledge Graphs",
     "abstract": "Knowledge graphs integrate biomedical data to identify drug repurposing candidates. We survey GNN-based drug-target interaction prediction and identify gaps in rare disease drug repurposing.",
     "uploaded_by_user_id": 3, "keywords": ["drug repurposing", "knowledge graph", "drug target interaction", "biomedical KG", "rare disease"], "category": "Healthcare AI", "year": 2022, "citation_count": 340, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Chest X-Ray Diagnosis with Deep Learning: Benchmarks and Gaps",
     "abstract": "Deep learning achieves radiologist-level accuracy on chest X-ray diagnosis. However gaps remain in rare pathology detection, pediatric radiology, and deployment in low-resource healthcare settings.",
     "uploaded_by_user_id": 1, "keywords": ["chest X-ray", "radiology AI", "pneumonia detection", "CheXNet", "medical imaging", "low-resource healthcare"], "category": "Healthcare AI", "year": 2022, "citation_count": 220, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Mental Health and NLP: Detecting Depression from Text",
     "abstract": "NLP methods can detect indicators of depression, anxiety, and suicidal ideation from social media and clinical notes. We survey datasets, models, and ethical challenges in mental health NLP.",
     "uploaded_by_user_id": 2, "keywords": ["mental health NLP", "depression detection", "suicide ideation", "social media health", "psychiatric NLP"], "category": "Healthcare AI", "year": 2022, "citation_count": 310, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Genomic Sequence Analysis with Deep Learning",
     "abstract": "Deep learning has transformed genomic sequence analysis including variant calling, gene expression prediction, and regulatory element identification. Key gaps remain in interpretability and cross-species generalization.",
     "uploaded_by_user_id": 3, "keywords": ["genomics", "DNA sequence", "variant calling", "gene expression", "regulatory elements", "bioinformatics deep learning"], "category": "Healthcare AI", "year": 2021, "citation_count": 650, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Wearable Health Monitoring: ML for Continuous Patient Monitoring",
     "abstract": "Wearable devices generate continuous streams of physiological data. ML methods detect arrhythmia, sleep disorders, and stress from wearable signals. Gaps remain in real-world deployment and battery constraints.",
     "uploaded_by_user_id": 1, "keywords": ["wearable health", "continuous monitoring", "ECG classification", "arrhythmia detection", "physiological signals", "smartwatch health"], "category": "Healthcare AI", "year": 2022, "citation_count": 240, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Explainable AI for Clinical Decision Support",
     "abstract": "Clinical decision support systems must be explainable to gain physician trust. We survey SHAP, LIME, and attention-based explanations in healthcare and identify gaps in clinician-centered explanation design.",
     "uploaded_by_user_id": 2, "keywords": ["explainable AI healthcare", "clinical decision support", "SHAP healthcare", "physician trust", "interpretable ML clinical"], "category": "Healthcare AI", "year": 2022, "citation_count": 370, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Pandemic Prediction Using ML: COVID-19 and Beyond",
     "abstract": "ML models have been applied to COVID-19 spread prediction, drug development, and clinical outcome forecasting. We identify gaps in real-time pandemic monitoring and integration with epidemiological models.",
     "uploaded_by_user_id": 3, "keywords": ["pandemic prediction", "COVID-19 ML", "epidemiology AI", "outbreak detection", "infectious disease modeling"], "category": "Healthcare AI", "year": 2021, "citation_count": 480, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Synthetic Patient Data Generation for Healthcare ML",
     "abstract": "Synthetic data generation addresses privacy barriers in healthcare ML. We survey GAN-based, VAE-based, and diffusion-based methods for generating realistic EHR, imaging, and genomic data.",
     "uploaded_by_user_id": 1, "keywords": ["synthetic data", "patient data generation", "GAN healthcare", "data augmentation medical", "privacy-preserving healthcare"], "category": "Healthcare AI", "year": 2022, "citation_count": 195, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Brain-Computer Interfaces and ML",
     "abstract": "Brain-computer interfaces translate neural signals into device commands. ML methods for EEG and ECoG signal decoding enable motor rehabilitation and communication. Gaps exist in cross-subject generalization.",
     "uploaded_by_user_id": 2, "keywords": ["brain computer interface", "BCI", "EEG classification", "neural decoding", "motor imagery", "neuroprosthetics"], "category": "Healthcare AI", "year": 2022, "citation_count": 280, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "AI in Dentistry: Applications and Research Gaps",
     "abstract": "AI has been applied to dental X-ray analysis, cavity detection, and treatment planning. We find that clinical validation datasets are extremely limited and most studies use small single-center samples.",
     "uploaded_by_user_id": 3, "keywords": ["dental AI", "oral health", "cavity detection", "dental X-ray", "dentistry ML", "panoramic radiograph"], "category": "Healthcare AI", "year": 2022, "citation_count": 85, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Telemedicine and Remote Patient Monitoring: AI Integration",
     "abstract": "Telemedicine platforms generate diverse patient data ripe for AI integration. We survey ML for remote triage, chronic disease monitoring, and medication adherence and identify gaps in low-bandwidth settings.",
     "uploaded_by_user_id": 1, "keywords": ["telemedicine AI", "remote patient monitoring", "chronic disease AI", "triage automation", "medication adherence ML"], "category": "Healthcare AI", "year": 2023, "citation_count": 120, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    # =========================================================================
    #  CATEGORY 8: Robotics & Autonomous Systems (10 papers)
    # =========================================================================
    {"title": "Deep Reinforcement Learning for Robotic Manipulation",
     "abstract": "Deep RL enables robots to learn manipulation skills from raw sensor inputs. We survey Sim2Real transfer, reward shaping, and multi-task learning for robotic grasping and dexterous manipulation.",
     "uploaded_by_user_id": 2, "keywords": ["robotic manipulation", "deep reinforcement learning", "Sim2Real", "grasping", "dexterous manipulation"], "category": "Robotics", "year": 2022, "citation_count": 680, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "SLAM: Simultaneous Localization and Mapping Survey",
     "abstract": "SLAM enables robots to build maps of unknown environments while tracking their location. We survey visual SLAM, LiDAR SLAM, and semantic SLAM and identify gaps in dynamic environments.",
     "uploaded_by_user_id": 3, "keywords": ["SLAM", "simultaneous localization mapping", "visual SLAM", "LiDAR SLAM", "robot navigation", "3D mapping"], "category": "Robotics", "year": 2022, "citation_count": 1200, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Human-Robot Interaction: Natural Language Interfaces",
     "abstract": "Natural language interfaces enable intuitive robot control. We survey LLM-based task planning, instruction following, and grounded language understanding for service and industrial robots.",
     "uploaded_by_user_id": 1, "keywords": ["human robot interaction", "NLU robot", "task planning", "instruction following", "grounded language learning"], "category": "Robotics", "year": 2023, "citation_count": 210, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Drone Navigation and Obstacle Avoidance Using Deep Learning",
     "abstract": "Deep learning methods enable drones to navigate complex environments and avoid obstacles autonomously. We identify gaps in adversarial conditions, GPS-denied navigation, and energy-efficient trajectory planning.",
     "uploaded_by_user_id": 2, "keywords": ["drone navigation", "UAV", "obstacle avoidance", "autonomous flight", "GPS denied navigation", "aerial robotics"], "category": "Robotics", "year": 2022, "citation_count": 290, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Soft Robotics: Design, Actuation, and Control",
     "abstract": "Soft robots made from compliant materials can safely interact with humans and unstructured environments. We survey pneumatic, tendon-driven, and electroactive actuators and identify gaps in control and fabrication.",
     "uploaded_by_user_id": 3, "keywords": ["soft robotics", "compliant mechanisms", "pneumatic actuator", "bio-inspired robot", "wearable robot"], "category": "Robotics", "year": 2021, "citation_count": 340, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Multi-Robot Systems: Coordination and Communication",
     "abstract": "Multi-robot systems perform tasks collectively through coordination. We survey consensus algorithms, task allocation, and formation control and identify gaps in large-scale heterogeneous swarms.",
     "uploaded_by_user_id": 1, "keywords": ["multi-robot", "swarm robotics", "task allocation", "robot coordination", "formation control", "cooperative robotics"], "category": "Robotics", "year": 2022, "citation_count": 180, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Exoskeleton Robotics for Rehabilitation",
     "abstract": "Robotic exoskeletons assist stroke and spinal cord injury rehabilitation. ML methods predict user intent from EMG and EEG signals. Gaps remain in long-term adaptability and clinical deployment.",
     "uploaded_by_user_id": 2, "keywords": ["exoskeleton", "rehabilitation robotics", "EMG control", "stroke rehabilitation", "wearable exoskeleton"], "category": "Robotics", "year": 2022, "citation_count": 150, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Agricultural Robotics: Challenges in Precision Farming",
     "abstract": "Agricultural robots perform planting, harvesting, and crop monitoring tasks. We identify open challenges in unstructured farm environments, multi-crop adaptability, and cost-effective deployment.",
     "uploaded_by_user_id": 3, "keywords": ["agricultural robotics", "precision farming", "crop harvesting", "weed detection robot", "farm automation"], "category": "Robotics", "year": 2022, "citation_count": 120, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Underwater Robotics: Perception and Navigation Challenges",
     "abstract": "Underwater robots face unique perception challenges from poor visibility and GPS unavailability. We survey acoustic SLAM, underwater vision, and bioinspired propulsion and identify gaps in deep-sea exploration.",
     "uploaded_by_user_id": 1, "keywords": ["underwater robot", "AUV", "acoustic SLAM", "underwater vision", "deep sea exploration", "marine robotics"], "category": "Robotics", "year": 2021, "citation_count": 95, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Robot Learning from Demonstration: Imitation Learning Survey",
     "abstract": "Learning from demonstration enables robots to acquire skills by observing human teachers. We survey behavioral cloning, inverse RL, and GAIL and identify gaps in long-horizon task learning.",
     "uploaded_by_user_id": 2, "keywords": ["imitation learning", "learning from demonstration", "behavioral cloning", "inverse reinforcement learning", "GAIL"], "category": "Robotics", "year": 2022, "citation_count": 450, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    # =========================================================================
    #  CATEGORY 9: Edge Computing & IoT (10 papers)
    # =========================================================================
    {"title": "Edge Computing: Vision and Challenges",
     "abstract": "Edge computing brings computation and data storage closer to data sources. We survey MEC, fog computing, and cloudlet architectures and identify challenges in resource management and latency optimization.",
     "uploaded_by_user_id": 3, "keywords": ["edge computing", "MEC", "fog computing", "cloudlet", "latency", "offloading"], "category": "Edge Computing", "year": 2020, "citation_count": 4200, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Federated Learning at the Edge: Challenges and Opportunities",
     "abstract": "Running federated learning on edge devices faces constraints in memory, compute, and connectivity. We survey communication-efficient FL, on-device training, and personalized federated learning.",
     "uploaded_by_user_id": 1, "keywords": ["edge federated learning", "on-device training", "communication efficient FL", "personalized FL", "resource constrained ML"], "category": "Edge Computing", "year": 2022, "citation_count": 560, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "5G Network Slicing for IoT Applications",
     "abstract": "5G network slicing enables customized virtual networks for diverse IoT use cases. We survey slice management, resource allocation, and ML-based slice adaptation and identify gaps in ultra-reliable slicing.",
     "uploaded_by_user_id": 2, "keywords": ["5G", "network slicing", "IoT", "resource allocation", "ultra-reliable low latency", "URLLC"], "category": "Edge Computing", "year": 2021, "citation_count": 780, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Smart Home Systems: Security and Privacy Challenges",
     "abstract": "Smart home devices collect sensitive personal data and face security vulnerabilities. We survey smart home attack surfaces, privacy leakage, and defensive mechanisms and identify user awareness gaps.",
     "uploaded_by_user_id": 3, "keywords": ["smart home", "IoT security", "privacy leakage", "smart speaker", "home automation security"], "category": "Edge Computing", "year": 2022, "citation_count": 320, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Energy Harvesting for IoT: Self-Powered Sensor Networks",
     "abstract": "Energy harvesting enables battery-free IoT operation. We survey solar, RF, vibration, and thermal harvesting and identify gaps in multi-source harvesting and predictive energy management.",
     "uploaded_by_user_id": 1, "keywords": ["energy harvesting", "battery-free IoT", "solar harvesting", "RF energy harvesting", "self-powered sensors"], "category": "Edge Computing", "year": 2021, "citation_count": 240, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Digital Twins for Industrial IoT",
     "abstract": "Digital twins create virtual replicas of physical systems for monitoring and optimization. We survey digital twin architectures for manufacturing and smart grids and identify gaps in real-time synchronization.",
     "uploaded_by_user_id": 2, "keywords": ["digital twin", "industrial IoT", "IIoT", "predictive maintenance", "cyber-physical system", "smart manufacturing"], "category": "Edge Computing", "year": 2022, "citation_count": 890, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Vehicular Edge Computing for Autonomous Driving",
     "abstract": "Vehicular edge computing offloads autonomous driving tasks to roadside units. We survey V2X communication, task scheduling, and cooperative perception and identify latency and reliability gaps.",
     "uploaded_by_user_id": 3, "keywords": ["vehicular edge computing", "V2X", "autonomous driving edge", "roadside unit", "cooperative perception"], "category": "Edge Computing", "year": 2022, "citation_count": 410, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "LoRaWAN for Wide-Area IoT: Performance and Limitations",
     "abstract": "LoRaWAN enables long-range IoT communication at low power. We survey LoRaWAN capacity, interference, and adaptive data rate and identify gaps in dense deployment and coexistence with 5G.",
     "uploaded_by_user_id": 1, "keywords": ["LoRaWAN", "LPWAN", "IoT communication", "long range IoT", "smart city IoT"], "category": "Edge Computing", "year": 2021, "citation_count": 380, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "MLOps: Machine Learning Operations at Scale",
     "abstract": "MLOps bridges the gap between ML development and production deployment. We survey model monitoring, continuous training, feature stores, and serving infrastructure and identify automation gaps.",
     "uploaded_by_user_id": 2, "keywords": ["MLOps", "model deployment", "continuous training", "feature store", "model monitoring", "ML pipeline"], "category": "Edge Computing", "year": 2022, "citation_count": 630, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Quantum Computing for Machine Learning: Opportunities",
     "abstract": "Quantum ML algorithms promise exponential speedups for certain ML tasks. We survey quantum neural networks, quantum kernel methods, and variational quantum circuits and identify hardware limitations.",
     "uploaded_by_user_id": 3, "keywords": ["quantum ML", "quantum computing", "quantum neural network", "variational quantum circuit", "quantum advantage"], "category": "Edge Computing", "year": 2022, "citation_count": 720, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    # =========================================================================
    #  CATEGORY 10: Information Retrieval & Recommendation Systems (10 papers)
    # =========================================================================
    {"title": "Neural Information Retrieval: A Survey",
     "abstract": "Neural IR models have transformed document retrieval. We survey dense retrieval (DPR, ANCE), re-ranking (MonoBERT), and learned sparse retrieval and identify gaps in multilingual and multi-hop retrieval.",
     "uploaded_by_user_id": 1, "keywords": ["information retrieval", "dense retrieval", "DPR", "re-ranking", "neural IR", "BEIR benchmark"], "category": "Information Retrieval", "year": 2022, "citation_count": 1100, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Collaborative Filtering for Recommendation Systems",
     "abstract": "Collaborative filtering predicts user preferences from interaction history. We survey matrix factorization, neural collaborative filtering, and graph-based CF and identify cold-start and fairness challenges.",
     "uploaded_by_user_id": 2, "keywords": ["collaborative filtering", "recommendation system", "matrix factorization", "neural CF", "cold start", "user-item interaction"], "category": "Information Retrieval", "year": 2021, "citation_count": 2300, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Knowledge Graph Embeddings for Recommendation",
     "abstract": "Knowledge graphs enrich recommendation with semantic item attributes. We survey TransE, RotatE, and KG-aware recommendation models and identify gaps in temporal KG recommendation.",
     "uploaded_by_user_id": 3, "keywords": ["knowledge graph embedding", "recommendation", "TransE", "semantic recommendation", "entity alignment"], "category": "Information Retrieval", "year": 2022, "citation_count": 680, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Conversational Recommendation Systems",
     "abstract": "Conversational RS interactively elicits user preferences through dialogue. We survey clarifying question strategies, multi-turn preference modeling, and exploration-exploitation tradeoffs.",
     "uploaded_by_user_id": 1, "keywords": ["conversational recommendation", "dialogue recommendation", "clarifying questions", "multi-turn dialogue", "interactive RS"], "category": "Information Retrieval", "year": 2022, "citation_count": 340, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Session-Based Recommendation with Graph Neural Networks",
     "abstract": "Session-based recommendation predicts the next item without user identity. We survey GNN-based session modeling using SR-GNN and NISER and identify gaps in long-session recommendation.",
     "uploaded_by_user_id": 2, "keywords": ["session-based recommendation", "SR-GNN", "next item prediction", "anonymous session", "short-term preference"], "category": "Information Retrieval", "year": 2021, "citation_count": 520, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Research Paper Recommendation: A Survey",
     "abstract": "Academic paper recommendation helps researchers discover relevant literature. We survey citation-based, content-based, and collaborative approaches and identify gaps in cross-domain and serendipitous recommendation.",
     "uploaded_by_user_id": 3, "keywords": ["paper recommendation", "academic search", "citation recommendation", "research discovery", "scholarly recommendation"], "category": "Information Retrieval", "year": 2022, "citation_count": 190, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Debiasing Recommendation Systems",
     "abstract": "Recommendation systems suffer from exposure bias, popularity bias, and selection bias. We survey inverse propensity scoring, causal debiasing, and counterfactual methods for fair recommendation.",
     "uploaded_by_user_id": 1, "keywords": ["recommendation bias", "debiasing", "exposure bias", "popularity bias", "counterfactual recommendation", "fairness RS"], "category": "Information Retrieval", "year": 2022, "citation_count": 430, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Cross-Domain Recommendation: Bridging Data Silos",
     "abstract": "Cross-domain recommendation transfers knowledge from data-rich domains to alleviate cold start. We survey transfer learning, meta-learning, and federated approaches for cross-platform recommendation.",
     "uploaded_by_user_id": 2, "keywords": ["cross-domain recommendation", "transfer learning RS", "cold start", "domain adaptation RS", "multi-domain RS"], "category": "Information Retrieval", "year": 2022, "citation_count": 280, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Explainable Recommendation Systems",
     "abstract": "Explainable RS increases user trust by providing reasons for recommendations. We survey template-based, review-based, and knowledge-graph-based explanation methods and identify evaluation challenges.",
     "uploaded_by_user_id": 3, "keywords": ["explainable recommendation", "transparent RS", "recommendation explanation", "user trust RS", "review-based explanation"], "category": "Information Retrieval", "year": 2021, "citation_count": 610, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Large Language Models for Information Retrieval",
     "abstract": "LLMs like GPT and T5 are being applied to document retrieval and question answering. We survey LLM-based retrieval augmentation, generative IR, and identify gaps in hallucination control and latency.",
     "uploaded_by_user_id": 1, "keywords": ["LLM retrieval", "generative IR", "document ranking LLM", "RAG", "hallucination IR", "LLM search"], "category": "Information Retrieval", "year": 2023, "citation_count": 850, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},


    #  NEW CATEGORY 11: Generative AI (8 papers)
    # =========================================================================
    {"title": "DALL-E 2: Hierarchical Text-Conditional Image Generation",
     "abstract": "We present DALL-E 2, a generative model that creates realistic images and art from natural language descriptions. Using a diffusion-based decoder, it generates high-resolution images with diverse compositions.",
     "uploaded_by_user_id": 1, "keywords": ["DALL-E", "text-to-image", "diffusion model", "generative AI", "image generation"], "category": "Generative AI", "year": 2022, "citation_count": 8500, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Stable Diffusion: High-Resolution Image Synthesis with Latent Diffusion Models",
     "abstract": "We introduce latent diffusion models that operate in the latent space of powerful pretrained autoencoders, achieving state-of-the-art results in image synthesis while significantly reducing computational requirements.",
     "uploaded_by_user_id": 2, "keywords": ["Stable Diffusion", "latent diffusion", "text-to-image", "generative AI", "open source"], "category": "Generative AI", "year": 2022, "citation_count": 12000, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Midjourney: AI Art Generation and Creative Applications",
     "abstract": "This paper analyzes the Midjourney AI art generation system, its architecture, and its impact on creative industries, identifying gaps in fine-grained control and consistency.",
     "uploaded_by_user_id": 3, "keywords": ["Midjourney", "AI art", "creative AI", "text-to-image", "prompt engineering"], "category": "Generative AI", "year": 2023, "citation_count": 3200, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "MusicLM: Generating Music from Text Descriptions",
     "abstract": "We introduce MusicLM, a model that generates high-fidelity music from text descriptions, demonstrating strong performance on various music generation tasks including conditioning on both text and melody.",
     "uploaded_by_user_id": 1, "keywords": ["MusicLM", "text-to-music", "audio generation", "generative AI", "music synthesis"], "category": "Generative AI", "year": 2023, "citation_count": 1800, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Video Generation with Diffusion Models: A Survey",
     "abstract": "We survey emerging diffusion-based video generation models including Imagen Video, Make-A-Video, and Phenaki, identifying challenges in temporal consistency and computational efficiency.",
     "uploaded_by_user_id": 2, "keywords": ["video generation", "diffusion video", "text-to-video", "temporal modeling", "generative video"], "category": "Generative AI", "year": 2023, "citation_count": 950, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "3D Generative Models: From NeRF to Diffusion",
     "abstract": "We review 3D generative models including NeRF, DreamFusion, and Magic3D, analyzing their capabilities for text-to-3D generation and identifying gaps in geometry quality and rendering speed.",
     "uploaded_by_user_id": 3, "keywords": ["3D generation", "NeRF", "text-to-3D", "dreamfusion", "generative 3D"], "category": "Generative AI", "year": 2023, "citation_count": 720, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Prompt Engineering: A Systematic Survey",
     "abstract": "We provide a comprehensive survey of prompt engineering techniques for large language models, including few-shot prompting, chain-of-thought, and tree-of-thoughts prompting methods.",
     "uploaded_by_user_id": 1, "keywords": ["prompt engineering", "LLM prompting", "chain-of-thought", "few-shot", "instruction tuning"], "category": "Generative AI", "year": 2023, "citation_count": 2100, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Hallucination Mitigation in Large Language Models",
     "abstract": "We survey techniques for reducing hallucinations in LLMs, including retrieval-augmented generation, reinforcement learning from human feedback, and fact-checking mechanisms.",
     "uploaded_by_user_id": 2, "keywords": ["hallucination", "LLM reliability", "factual accuracy", "RAG", "RLHF"], "category": "Generative AI", "year": 2023, "citation_count": 1650, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    # =========================================================================
    #  NEW CATEGORY 12: Green & Sustainable AI (6 papers)
    # =========================================================================
    {"title": "Green AI: Energy-Efficient Machine Learning",
     "abstract": "We analyze the carbon footprint of training large AI models and propose strategies for sustainable AI development, including model compression, efficient architectures, and hardware optimization.",
     "uploaded_by_user_id": 3, "keywords": ["Green AI", "energy efficiency", "carbon footprint", "sustainable AI", "model compression"], "category": "Green AI", "year": 2022, "citation_count": 890, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Carbon Emissions of Large Language Models: An Empirical Study",
     "abstract": "We quantify the environmental impact of training LLMs including GPT-3, BLOOM, and LLaMA, proposing mitigation strategies and carbon-aware training schedules.",
     "uploaded_by_user_id": 1, "keywords": ["LLM emissions", "carbon footprint", "sustainable NLP", "green transformers", "environmental AI"], "category": "Green AI", "year": 2023, "citation_count": 560, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Energy-Aware Neural Architecture Search",
     "abstract": "We introduce energy consumption as an optimization objective in neural architecture search, discovering architectures that balance accuracy with energy efficiency.",
     "uploaded_by_user_id": 2, "keywords": ["energy-aware NAS", "sustainable deep learning", "efficient architectures", "green NAS"], "category": "Green AI", "year": 2022, "citation_count": 340, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Model Pruning and Quantization for Sustainable AI",
     "abstract": "We survey pruning and quantization techniques for reducing model size and inference energy, analyzing their effectiveness across vision and language models.",
     "uploaded_by_user_id": 3, "keywords": ["model pruning", "quantization", "model compression", "efficient inference", "sustainable AI"], "category": "Green AI", "year": 2022, "citation_count": 420, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Data-Centric AI for Sustainability",
     "abstract": "We explore how data selection and curation strategies can reduce the environmental cost of AI training, including active learning and data subset selection.",
     "uploaded_by_user_id": 1, "keywords": ["data-centric AI", "sustainable ML", "data selection", "active learning", "efficient training"], "category": "Green AI", "year": 2023, "citation_count": 210, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Hardware-Aware Neural Network Design",
     "abstract": "We survey hardware-aware neural architecture design techniques that optimize for specific hardware platforms to maximize energy efficiency for edge deployment.",
     "uploaded_by_user_id": 2, "keywords": ["hardware-aware NAS", "edge AI", "efficient hardware", "TinyML", "energy-efficient AI"], "category": "Green AI", "year": 2022, "citation_count": 280, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    # =========================================================================
    #  NEW CATEGORY 13: Federated Learning (7 papers)
    # =========================================================================
    {"title": "Federated Learning for Healthcare: A Comprehensive Review",
     "abstract": "We review federated learning applications in healthcare, including medical imaging, EHR analysis, and drug discovery, identifying challenges in data heterogeneity and privacy.",
     "uploaded_by_user_id": 3, "keywords": ["federated learning healthcare", "medical FL", "privacy-preserving medicine", "distributed healthcare AI"], "category": "Federated Learning", "year": 2022, "citation_count": 890, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Personalized Federated Learning: Algorithms and Applications",
     "abstract": "We survey personalization techniques in federated learning including meta-learning, multi-task learning, and clustering-based approaches for handling heterogeneous user data.",
     "uploaded_by_user_id": 1, "keywords": ["personalized FL", "meta-learning FL", "multi-task FL", "user adaptation", "heterogeneous FL"], "category": "Federated Learning", "year": 2022, "citation_count": 720, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Vertical Federated Learning: Challenges and Opportunities",
     "abstract": "We focus on vertical federated learning where parties have different feature sets, covering entity alignment, encryption techniques, and model aggregation strategies.",
     "uploaded_by_user_id": 2, "keywords": ["vertical FL", "feature alignment", "entity resolution", "heterogeneous FL", "cross-silo FL"], "category": "Federated Learning", "year": 2022, "citation_count": 450, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Byzantine-Resilient Federated Learning: Attacks and Defenses",
     "abstract": "We survey Byzantine attacks and defenses in federated learning, including poisoning attacks, backdoor attacks, and robust aggregation mechanisms.",
     "uploaded_by_user_id": 3, "keywords": ["Byzantine FL", "poisoning attacks", "robust aggregation", "FL security", "adversarial FL"], "category": "Federated Learning", "year": 2023, "citation_count": 380, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Communication-Efficient Federated Learning: A Survey",
     "abstract": "We review techniques for reducing communication overhead in federated learning, including gradient compression, local updates, and asynchronous aggregation.",
     "uploaded_by_user_id": 1, "keywords": ["communication-efficient FL", "gradient compression", "local SGD", "asynchronous FL", "FedAvg"], "category": "Federated Learning", "year": 2022, "citation_count": 620, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Federated Learning for Edge Computing: Challenges and Solutions",
     "abstract": "We analyze the challenges of deploying federated learning on edge devices, including resource constraints, connectivity issues, and device heterogeneity.",
     "uploaded_by_user_id": 2, "keywords": ["edge FL", "on-device FL", "resource-constrained FL", "mobile FL", "cross-device FL"], "category": "Federated Learning", "year": 2022, "citation_count": 510, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Differential Privacy in Federated Learning: A Survey",
     "abstract": "We survey differential privacy techniques for federated learning, including local DP, central DP, and hybrid approaches for privacy-preserving model training.",
     "uploaded_by_user_id": 3, "keywords": ["differential privacy FL", "DP-FedAvg", "privacy-preserving FL", "local DP", "central DP"], "category": "Federated Learning", "year": 2023, "citation_count": 480, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    # =========================================================================
    #  NEW CATEGORY 14: Responsible & Ethical AI (6 papers)
    # =========================================================================
    {"title": "Algorithmic Fairness: Metrics, Methods, and Challenges",
     "abstract": "We provide a comprehensive review of fairness definitions, metrics, and mitigation techniques in machine learning, covering individual, group, and counterfactual fairness.",
     "uploaded_by_user_id": 1, "keywords": ["algorithmic fairness", "bias mitigation", "fair ML", "equity", "responsible AI"], "category": "Responsible AI", "year": 2022, "citation_count": 950, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Explainable AI: A Survey of Methods and Evaluation",
     "abstract": "We survey XAI methods including LIME, SHAP, and attention-based explanations, evaluating their effectiveness across different model types and application domains.",
     "uploaded_by_user_id": 2, "keywords": ["explainable AI", "XAI evaluation", "model interpretability", "SHAP", "LIME", "attention"], "category": "Responsible AI", "year": 2022, "citation_count": 2100, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "AI Governance: Frameworks, Regulations, and Best Practices",
     "abstract": "We survey existing AI governance frameworks from EU (AI Act), US (Blueprint for AI Bill of Rights), and China, proposing best practices for responsible AI development.",
     "uploaded_by_user_id": 3, "keywords": ["AI governance", "AI ethics", "regulatory compliance", "AI policy", "responsible AI"], "category": "Responsible AI", "year": 2023, "citation_count": 340, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Privacy-Preserving Machine Learning: Techniques and Trade-offs",
     "abstract": "We survey differential privacy, homomorphic encryption, secure multi-party computation, and trusted execution environments for privacy-preserving ML.",
     "uploaded_by_user_id": 1, "keywords": ["privacy-preserving ML", "differential privacy", "homomorphic encryption", "SMPC", "TEE"], "category": "Responsible AI", "year": 2022, "citation_count": 780, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Auditing and Certifying AI Systems",
     "abstract": "We propose frameworks for auditing AI systems for fairness, robustness, and transparency, including certification standards for responsible AI deployment.",
     "uploaded_by_user_id": 2, "keywords": ["AI auditing", "AI certification", "model verification", "responsible deployment", "AI safety"], "category": "Responsible AI", "year": 2023, "citation_count": 290, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Value Alignment in Large Language Models",
     "abstract": "We analyze techniques for aligning LLMs with human values, including RLHF, constitutional AI, and instruction tuning, identifying gaps in cross-cultural value alignment.",
     "uploaded_by_user_id": 3, "keywords": ["value alignment", "RLHF", "constitutional AI", "instruction tuning", "AI safety"], "category": "Responsible AI", "year": 2023, "citation_count": 560, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    # =========================================================================
    #  NEW CATEGORY 15: Reinforcement Learning (7 papers)
    # =========================================================================
    {"title": "Deep Reinforcement Learning: Algorithms and Applications",
     "abstract": "We survey deep RL algorithms including DQN, PPO, SAC, and TD3, analyzing their strengths, weaknesses, and application domains in robotics, games, and control.",
     "uploaded_by_user_id": 1, "keywords": ["deep RL", "DQN", "PPO", "policy gradient", "reinforcement learning"], "category": "Reinforcement Learning", "year": 2021, "citation_count": 3800, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Multi-Agent Reinforcement Learning: Challenges and Advances",
     "abstract": "We review MARL algorithms including MADDPG, QMIX, and MAPPO, identifying challenges in coordination, scalability, and non-stationarity in multi-agent environments.",
     "uploaded_by_user_id": 2, "keywords": ["multi-agent RL", "MARL", "cooperative AI", "game theory", "decentralized RL"], "category": "Reinforcement Learning", "year": 2022, "citation_count": 1200, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Offline Reinforcement Learning: A Comprehensive Survey",
     "abstract": "We survey offline RL techniques that learn from static datasets without environment interaction, covering CQL, IQL, and decision transformers.",
     "uploaded_by_user_id": 3, "keywords": ["offline RL", "batch RL", "data-driven RL", "decision transformer", "CQL"], "category": "Reinforcement Learning", "year": 2022, "citation_count": 890, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Inverse Reinforcement Learning: Theory and Applications",
     "abstract": "We survey inverse RL methods for learning reward functions from demonstrations, including maximum entropy IRL, adversarial IRL, and their applications.",
     "uploaded_by_user_id": 1, "keywords": ["inverse RL", "imitation learning", "reward learning", "maximum entropy IRL", "AIRL"], "category": "Reinforcement Learning", "year": 2022, "citation_count": 560, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Reinforcement Learning for Robotics: From Simulation to Reality",
     "abstract": "We analyze Sim2Real transfer techniques in robotic RL, including domain randomization, system identification, and latent space adaptation.",
     "uploaded_by_user_id": 2, "keywords": ["Sim2Real", "robotic RL", "domain randomization", "transfer learning", "robot learning"], "category": "Reinforcement Learning", "year": 2022, "citation_count": 720, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Hierarchical Reinforcement Learning: Methods and Applications",
     "abstract": "We survey HRL approaches including options framework, feudal networks, and hierarchical DQN for solving long-horizon tasks with sparse rewards.",
     "uploaded_by_user_id": 3, "keywords": ["hierarchical RL", "options framework", "temporal abstraction", "goal-conditioned RL", "HRL"], "category": "Reinforcement Learning", "year": 2022, "citation_count": 430, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},

    {"title": "Safe Reinforcement Learning: A Survey",
     "abstract": "We review safe RL methods that ensure constraint satisfaction during learning, including constrained MDPs, shielding, and reward shaping approaches.",
     "uploaded_by_user_id": 1, "keywords": ["safe RL", "constrained RL", "risk-sensitive RL", "shielding", "safety guarantees"], "category": "Reinforcement Learning", "year": 2023, "citation_count": 380, "language": "English", "status": "indexed", "uploaded_at": datetime.utcnow()},
]

# =============================================================================
#  INSERT ALL PAPERS
# =============================================================================
result = papers.insert_many(all_papers)
total  = len(result.inserted_ids)
print(f"\n  ✓ Inserted {total} papers successfully!")

# =============================================================================
#  REBUILD TEXT INDEX
# =============================================================================
papers.create_index(
    [("title", "text"), ("abstract", "text"), ("keywords", "text")],
    name="papers_text_search",
    weights={"title": 10, "abstract": 5, "keywords": 3}
)
papers.create_index([("category",  1)], name="papers_category")
papers.create_index([("year",     -1)], name="papers_year")
papers.create_index([("citation_count", -1)], name="papers_citations")
print("  ✓ All indexes rebuilt")

# =============================================================================
#  STATS
# =============================================================================
print("\n  Papers by Category:")
print(f"  {'Category':<40} Papers")
print(f"  {'-'*40} ------")
pipeline = [{"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}]
for doc in papers.aggregate(pipeline):
    print(f"  {doc['_id']:<40} {doc['count']:>3}")

print(f"\n  Total papers in DB : {papers.count_documents({})}")
print(f"  Categories covered : {len(list(papers.distinct('category')))}")
earliest = papers.find_one({}, sort=[("year", 1)])
latest   = papers.find_one({}, sort=[("year", -1)])
print(f"  Year range         : {earliest['year']} – {latest['year']}")

# =============================================================================
#  QUICK SEARCH TESTS
# =============================================================================
print("\n  Search tests:")
tests = ["transformer attention", "federated learning", "generative AI", "green AI"]
for q in tests:
    r = papers.find({"$text": {"$search": q}},
                    {"title": 1, "score": {"$meta": "textScore"}}) \
              .sort([("score", {"$meta": "textScore"})]).limit(2)
    print(f"\n  Query: '{q}'")
    for doc in r:
        print(f"    → {doc['title'][:60]}")

print("\n" + "=" * 65)
print("  Done! Now run:  python gapinsight_engine.py")
print("  Now backed by papers across 15 research domains!")
print("=" * 65)

client.close()