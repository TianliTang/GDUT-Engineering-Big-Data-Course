# Python建模与调参

基本步骤：建立模型对象→fit训练→predict_proba输出概率→在验证集评价。主要超参数包括max_depth、min_samples_split、min_samples_leaf和max_leaf_nodes。调参时同时查看验证指标、训练—验证差距和叶节点数。
