import React from "react";
import {
  ErrorBoundary,
  Facet,
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  Sorting,
  WithSearch
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";
import CustomConnector from "./connector"
const connector = new CustomConnector();

/*
import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";
const connector = new ElasticsearchAPIConnector({
  host: "http://localhost:9200",
  index: "esci-products"
});
*/

const config = {
  searchQuery: {
    search_fields: {
      "product_title.ja": {
        weight: 3
      },
      "product_description.ja": {},
      "product_bullet_point.ja": {}
    },
    result_fields: {
      product_id: {},
      product_brand: {},
      product_title: {},
      "product_title.ja": {
        snippet: {
          size: 3,
          fallback: true
        }
      },
      "product_description.ja": {
        snippet: {
          size: 100,
          fallback: true
        }
      }
    },
    disjunctiveFacets: ["product_color", "product_brand", "product_locale"],
    facets: {
      "product_locale": { type: "value" },
      "product_brand": { type: "value" },
      "product_color": { type: "value" }
    }
  },
  apiConnector: connector,
  alwaysSearchOnInitialLoad: true
};

export default function App() {
  return (
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => {
          return (
            <div className="App">
              <ErrorBoundary>
                <Layout
                  header={<SearchBox autocompleteSuggestions={false} />}
                  sideContent={
                    <div>
                      {wasSearched && (
                        <Sorting
                          label={"Sort by"}
                          sortOptions={[]}
                        />
                      )}
                      <Facet key={"1"} field={"product_locale"} label={"locales"} />
                      <Facet key={"2"} field={"product_brand"} label={"brands"} />
                      <Facet key={"3"} field={"product_color"} label={"colors"} />
                    </div>
                  }
                  bodyContent={
                    <Results
                      titleField={"product_title.ja"}
                      shouldTrackClickThrough={true}
                    />
                  }
                  bodyHeader={
                    <React.Fragment>
                      {wasSearched && <PagingInfo />}
                      {wasSearched && <ResultsPerPage />}
                    </React.Fragment>
                  }
                  bodyFooter={<Paging />}
                />
              </ErrorBoundary>
            </div>
          );
        }}
      </WithSearch>
    </SearchProvider>
  );
}
