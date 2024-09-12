# theory

Vector databases are specialized databases designed to store and retrieve high-dimensional vector embeddings efficiently. These embeddings are often the result of machine learning models (e.g., word embeddings, image embeddings) and are used for tasks like similarity search, clustering, and recommendation systems.

### 1. **Storage of Vector Embeddings**

Vector databases store vector embeddings in a structured way to allow for efficient retrieval. Here’s how it’s typically done:

#### a. **Data Structure**:
- **Flat Files or Arrays**: In simpler implementations, embeddings are stored as flat files or in arrays within a database, where each vector is associated with a unique identifier (e.g., a document ID, image ID).
- **Key-Value Stores**: Some vector databases use key-value stores where the key is the identifier, and the value is the vector embedding.
- **Advanced Index Structures**: More advanced vector databases use specialized data structures to enable efficient search and retrieval:
  - **Spatial Trees**: Trees like KD-Tree, Ball Tree, or VP-Tree are used to partition the vector space hierarchically.
  - **Quantization-Based Methods**: Product Quantization (PQ) or Hierarchical Navigable Small World (HNSW) graphs are used to approximate the vector space efficiently.

#### b. **Compression**:
- **Dimensionality Reduction**: Techniques like Principal Component Analysis (PCA) or t-SNE may be used to reduce the dimensionality of vectors, reducing storage space while maintaining most of the important information.
- **Quantization**: Vectors are compressed using quantization techniques, which reduce the precision of vector components to save space.

### 2. **Efficient Retrieval**

Retrieving vector embeddings efficiently, especially in large-scale databases, is critical. Here’s how it’s done:

#### a. **Indexing Methods**:
Vector databases often use advanced indexing methods tailored for high-dimensional spaces:

- **Approximate Nearest Neighbor (ANN) Search**:
  - **LSH (Locality-Sensitive Hashing)**: LSH hashes similar vectors to the same bucket with high probability, allowing for fast similarity searches by only checking within the same or nearby buckets.
  - **HNSW (Hierarchical Navigable Small World Graphs)**: HNSW is a graph-based method that navigates through nodes (vectors) in a hierarchical fashion, enabling quick retrieval of approximate nearest neighbors.
  - **IVF (Inverted File Index)**: The vector space is partitioned into cells, and vectors are assigned to these cells. At search time, only relevant cells are searched, reducing the search space.

- **Exact Nearest Neighbor Search**:
  - For smaller datasets or cases where exact retrieval is necessary, structures like KD-Trees, R-Trees, or Ball Trees can be used.

#### b. **Distance Metrics**:
- **Cosine Similarity**: Measures the cosine of the angle between two vectors, often used in text and document retrieval.
- **Euclidean Distance**: Measures the straight-line distance between two vectors, commonly used in image and video retrieval.
- **Dot Product**: Often used in collaborative filtering and recommendation systems.

#### c. **Parallelization and Distributed Computing**:
- **Sharding**: The vector space is divided into smaller shards, each stored on a different server. Queries are distributed across these servers and aggregated to return the final result.
- **GPU Acceleration**: GPUs can be used to speed up the computation of distance metrics and the processing of large datasets, leveraging their ability to perform parallel computations efficiently.

### 3. **Example Implementations**

Some popular vector databases and libraries include:

- **FAISS (Facebook AI Similarity Search)**:
  - An open-source library that provides both exact and approximate nearest neighbor search, optimized for large-scale vector similarity search.
  
- **Annoy (Approximate Nearest Neighbors Oh Yeah)**:
  - A C++ library with Python bindings for performing ANN search, commonly used in recommendation systems.
  
- **Milvus**:
  - An open-source vector database that supports both scalar data and vector data, with built-in support for various indexing algorithms like IVF, HNSW, and PQ.

### 4. **Example Workflow**

1. **Ingesting Vectors**:
   - Embeddings are generated using a machine learning model (e.g., BERT for text, ResNet for images).
   - Each embedding is stored in the vector database along with its identifier.

2. **Indexing**:
   - The database builds an index using one of the advanced methods mentioned above (e.g., HNSW, IVF).

3. **Querying**:
   - When querying, a vector embedding is generated for the query object.
   - The database uses the index to efficiently find vectors that are close to the query vector according to a defined distance metric.

4. **Result**:
   - The database returns identifiers of the closest vectors, often with a similarity score.

### Conclusion
Vector databases optimize both storage and retrieval of high-dimensional vector embeddings using specialized data structures, indexing methods, and parallel processing. Whether you choose exact or approximate nearest neighbor search, the approach depends on your specific use case, balancing speed, accuracy, and resource utilization.