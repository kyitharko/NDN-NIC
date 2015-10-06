#ifndef NDNNIC_BF_BLOOM_FILTER_HPP
#define NDNNIC_BF_BLOOM_FILTER_HPP

#include <string>

namespace ndnnic {

/** \brief implements a counting Bloom filter with false positive indication
 */
class BloomFilter
{
public:
  typedef std::basic_string<uint8_t> Key;
  typedef uint32_t Counter;

  /** \brief construct a Bloom filter
   *  \param capacity size of Bloom filter, in buckets
   *  \param nHashFunctions number of hash functions
   */
  BloomFilter(size_t capacity, size_t nHashFunctions);

  /** \brief insert a key
   *  \throw std::overflow_error any bucket would overflow after insertion
   */
  void
  insert(const Key& key);

  /** \brief erase a key
   *  \throw std::underflow_error any bucket would underflow after deletion,
   *                              which indicates the key doesn't exist
   */
  void
  erase(const Key& key);

  enum class LookupResult {
    NO,
    YES,
    FP
  };

  /** \brief lookup a key
   *  \retval NO the key doesn't exist
   *  \retval YES the key exists, and it's not a false positive
   *  \retval FP the key exists due to false positive
   */
  LookupResult
  lookup(const Key& key) const;

private:
  std::vector<Counter> m_buckets;
  std::unordered_multiset<Key> m_table;
};

} // namespace ndnnic

#endif // NDNNIC_BF_BLOOM_FILTER_HPP
