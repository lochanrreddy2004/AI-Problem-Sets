import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    pagelinks = corpus[page]
    total_page_count = len(corpus.keys())

    TM = {}

    if len(pagelinks) == 0:
        for key in corpus.keys():
            TM[key] = 1 / total_page_count
    else:
        for key in corpus.keys():
            if key in pagelinks:
                TM[key] = ((1 - damping_factor) / total_page_count) + (damping_factor / len(pagelinks))
            else:
                TM[key] = (1 - damping_factor) / total_page_count

    return TM



def sample_pagerank(corpus, damping_factor, n):
    pages = list(corpus.keys())
    current_page = random.choice(pages)
    page_rank = dict.fromkeys(corpus.keys(),0)

    for i in range(n):
        page_rank[current_page] += 1
        tm = transition_model(corpus=corpus,page=current_page,damping_factor=damping_factor)
        current_page = random.choices(pages,weights=[tm[p] for p in pages])[0]

    for page in page_rank:
        page_rank[page] /= n

    return page_rank

def iterate_pagerank(corpus, damping_factor):
    pages = list(corpus.keys())
    new_page_rank = dict.fromkeys(corpus.keys(),(1 / len(pages)))
    
    for page in corpus.keys():
        if not corpus[page]:
            corpus[page] = set(corpus.keys())

    converged = False
    while not converged:
        converged = True
        page_rank = new_page_rank.copy()

        for page in corpus:
            total = 0
            for possible_pages in corpus:
                if page in corpus[possible_pages]:
                    total += page_rank[possible_pages] / len(corpus[possible_pages])
            new_page_rank[page] = ((1 - damping_factor) / len(pages)) + (damping_factor * total)

        for p in corpus:
            if abs(page_rank[p] - new_page_rank[p]) > 0.001:
                converged = False
        
    return new_page_rank

if __name__ == "__main__":
    main()
