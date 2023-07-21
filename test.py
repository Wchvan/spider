import requests
query = '''
        query reviews($itemId: String!, $searchTerm: String, $sortBy: String, $startIndex: Int, $recfirstpage: String, $pagesize: String, $filters: ReviewsFilterInput) {
          reviews(itemId: $itemId, searchTerm: $searchTerm, sortBy: $sortBy, startIndex: $startIndex, recfirstpage: $recfirstpage, pagesize: $pagesize, filters: $filters) {
            Results {
              AuthorId
              Badges {
                DIY {
                  BadgeType
                  __typename
                }
                top250Contributor {
                  BadgeType
                  __typename
                }
                IncentivizedReview {
                  BadgeType
                  __typename
                }
                EarlyReviewerIncentive {
                  BadgeType
                  __typename
                }
                top1000Contributor {
                  BadgeType
                  __typename
                }
                VerifiedPurchaser {
                  BadgeType
                  __typename
                }
                __typename
              }
              BadgesOrder
              CampaignId
              ContextDataValues {
                Age {
                  Value
                  __typename
                }
                VerifiedPurchaser {
                  Value
                  __typename
                }
                __typename
              }
              ContextDataValuesOrder
              Id
              IsRecommended
              IsSyndicated
              Photos {
                Id
                Sizes {
                  normal {
                    Url
                    __typename
                  }
                  thumbnail {
                    Url
                    __typename
                  }
                  __typename
                }
                __typename
              }
              ProductId
              SubmissionTime
              TagDimensions {
                Pro {
                  Values
                  __typename
                }
                Con {
                  Values
                  __typename
                }
                __typename
              }
              Title
              TotalNegativeFeedbackCount
              TotalPositiveFeedbackCount
              ClientResponses {
                Response
                Date
                Department
                __typename
              }
              Rating
              RatingRange
              ReviewText
              SecondaryRatings {
                Quality {
                  Label
                  Value
                  __typename
                }
                Value {
                  Label
                  Value
                  __typename
                }
                EnergyEfficiency {
                  Label
                  Value
                  __typename
                }
                Features {
                  Label
                  Value
                  __typename
                }
                Appearance {
                  Label
                  Value
                  __typename
                }
                EaseOfInstallation {
                  Label
                  Value
                  __typename
                }
                EaseOfUse {
                  Label
                  Value
                  __typename
                }
                __typename
              }
              SecondaryRatingsOrder
              SyndicationSource {
                LogoImageUrl
                Name
                __typename
              }
              UserNickname
              UserLocation
              Videos {
                VideoId
                VideoThumbnailUrl
                VideoUrl
                __typename
              }
              __typename
            }
            Includes {
              Products {
                store {
                  Id
                  FilteredReviewStatistics {
                    AverageOverallRating
                    TotalReviewCount
                    TotalRecommendedCount
                    RecommendedCount
                    NotRecommendedCount
                    SecondaryRatingsAveragesOrder
                    RatingDistribution {
                      RatingValue
                      Count
                      __typename
                    }
                    ContextDataDistribution {
                      Age {
                        Values {
                          Value
                          Count
                          __typename
                        }
                        __typename
                      }
                      Gender {
                        Values {
                          Value
                          Count
                          __typename
                        }
                        __typename
                      }
                      Expertise {
                        Values {
                          Value
                          __typename
                        }
                        __typename
                      }
                      HomeGoodsProfile {
                        Values {
                          Value
                          Count
                          __typename
                        }
                        __typename
                      }
                      VerifiedPurchaser {
                        Values {
                          Value
                          Count
                          __typename
                        }
                        __typename
                      }
                      __typename
                    }
                    __typename
                  }
                  __typename
                }
                items {
                  Id
                  FilteredReviewStatistics {
                    AverageOverallRating
                    TotalReviewCount
                    TotalRecommendedCount
                    RecommendedCount
                    NotRecommendedCount
                    SecondaryRatingsAveragesOrder
                    RatingDistribution {
                      RatingValue
                      Count
                      __typename
                    }
                    ContextDataDistribution {
                      Age {
                        Values {
                          Value
                          Count
                          __typename
                        }
                        __typename
                      }
                      Gender {
                        Values {
                          Value
                          Count
                          __typename
                        }
                        __typename
                      }
                      Expertise {
                        Values {
                          Value
                          __typename
                        }
                        __typename
                      }
                      HomeGoodsProfile {
                        Values {
                          Value
                          Count
                          __typename
                        }
                        __typename
                      }
                      VerifiedPurchaser {
                        Values {
                          Value
                          Count
                          __typename
                        }
                        __typename
                      }
                      __typename
                    }
                    __typename
                  }
                  __typename
                }
                __typename
              }
              __typename
            }
            FilterSelected {
              StarRatings {
                is5Star
                is4Star
                is3Star
                is2Star
                is1Star
                __typename
              }
              VerifiedPurchaser
              SearchText
              __typename
            }
            pagination {
              previousPage {
                label
                isNextPage
                isPreviousPage
                isSelectedPage
                __typename
              }
              pages {
                label
                isNextPage
                isPreviousPage
                isSelectedPage
                __typename
              }
              nextPage {
                label
                isNextPage
                isPreviousPage
                isSelectedPage
                __typename
              }
              __typename
            }
            SortBy {
              mosthelpfull
              newest
              oldest
              highestrating
              lowestrating
              photoreview
              __typename
            }
            TotalResults
            __typename
          }
        }
        '''

data = {
    "operationName": "reviews",
    "variables": {
        "filters": {
            "isVerifiedPurchase": False,
            "prosCons": None,
            "starRatings": None
        },
        "itemId": "207167048",
        "pagesize": "10",
        "recfirstpage": "10",
        "searchTerm": None,
        "sortBy": "photoreview",
        "startIndex": 1
    },
    "query": query
}

headers = {
    "Origin": "https://www.homedepot.com",
    "Content-Type": "application/json",
    "Connection": "keep-alive",
    'Cookie': "HD_DC=origin; THD_NR=1; at_check=true; AMCVS_F6421253512D2C100A490D45%40AdobeOrg=1; THD_PERSIST=; THD_SESSION=; THD_CACHE_NAV_SESSION=; THD_CACHE_NAV_PERSIST=; thda.s=7b948c12-67d8-8a14-e6bb-da23b80798d7; thda.u=1c30d970-9527-b7c5-bea8-a52a5c833ccd; _px_f394gi7Fvmc43dfg_user_id=MTY0ZjI2ZjAtMjVkMi0xMWVlLWEwM2MtYmJlYjA1MWFiOTk3; ajs_anonymous_id=795c4522-9496-4723-9f54-b66e25f31068; thda.m=63435304895171780006669389195090073293; aam_uuid=63725623662432959736694938158043216056; QuantumMetricUserID=458da72a815da0f5a7691060668d6c04; LPVID=I4N2Y0NDU3OWVkZDg0MmIx; DELIVERY_ZIP=16803; DELIVERY_ZIP_TYPE=USER; QuantumMetricSessionID=c74050f741f35afbb9854395927dcb3a; AKA_A2=A; bm_sz=B3A08B0DFC02737886462B9999D31CD0~YAAQBC0+F8IoPWiJAQAAmKqwbBSF9lX0tfkiD47Z2qZOJ/i01GATLA6HK/9qQE4UU+71HDeusjoXLgvQiO/GiyXbLaC8O6yrK6Tg9qjRt7YUoXY32aJSz6zB5tTlZ+0vQnNVrPUhdvwWEI3vuaEFygKNefEOrO2qMhsvlSpsiVcqMOrk21uHHfjj0FmPcLfC5PlHkZLk1d4NAhgOmJomJv6YwJSr22WaVcJPY4J5vzZjmjg3VP6bS/Cgbn97trzMCprLE5jFgy55rCo8XzLHhkizy4eGjt4TLvuCp280ANetzbCOA9c=~3225923~3556420; ak_bmsc=47CCEF11B809048AB29EBB147B0F64AD~000000000000000000000000000000~YAAQBC0+F+UsPWiJAQAAJriwbBTkjmsBGdd5O2da8k97er/YuXop/kPdJrBetnRs+uEc7B+eGFhJSD/BQSccZRh/v69aG5COAAwlPb1HDKBX92AneV93GOUm0abKYFJltr0QmfKxXOV7qK6cFrNt4mlj3m2nS7N2/tASz1vF17ocXeEiURDqKfgzm49acWnPJtb92KYzbSYsWHrHkUlTYvi722I7JH0h28Dk7siI1jNg3jV6kIFrgz6EomWC2b16WYES9c5yZNWFwxaYtlU2IR9FeAex81hvezL5Fds1VpCOykm4ZS0qy4MLZyNfasqMQqVQguGKb6jr7PMojZCPTqFyJx/gW+/Ns/7dk3HlhS8MU4qd4eeQ9sMMgkfIu6BWP0r6k+z7vNHynrXgAvbLuF5siH5wmBcXDLs0wNX/WPVd+EysykzbOjYPhNFd3TxLOM5kpZCqYnTvWCunmLpWUbdnVyS2F0TBYi8DiRI5qAgD9BPbLNYXHRjDLG/+NJk=; THD_LOCALIZER=%7B%22WORKFLOW%22%3A%22LOC_HISTORY_BY_IP%22%2C%22THD_FORCE_LOC%22%3A%221%22%2C%22THD_INTERNAL%22%3A%220%22%2C%22THD_LOCSTORE%22%3A%221861%2BSan%20Jose%20(ge)%20-%20San%20Jose%2C%20CA%2B%22%2C%22THD_STRFINDERZIP%22%3A%2295125%22%2C%22THD_STORE_HOURS%22%3A%221%3B7%3A00-20%3A00%3B2%3B6%3A00-21%3A00%3B3%3B6%3A00-21%3A00%3B4%3B6%3A00-21%3A00%3B5%3B6%3A00-21%3A00%3B6%3B6%3A00-21%3A00%3B7%3B6%3A00-21%3A00%22%2C%22THD_STORE_HOURS_EXPIRY%22%3A1689749275%7D; mbox=PC#034466e1f7cb4d2485e6ec0bafa98e0c.35_0#1752990508|session#cade3b02b3544558866193de36a3d595#1689747568; forterToken=f3a820b5f941447aa36a83d23b80d047_1689745716356__UDF43_13ck; s_sess=%20s_pv_pName%3Dproductdetails%253E207167048%3B%20s_pv_pType%3Dpip%3B%20s_pv_cmpgn%3D%3B%20s_pv_pVer%3Dhd%2520home%2520v1%3B%20s_cc%3Dtrue%3B%20stsh%3D%3B; _abck=A10B984E58D70DEE679B7B307E824BDF~0~YAAQBC0+F+NpPWiJAQAAbYWxbAqPLtmC1bUd5jY/DwLsuBAVbjpDNH+wiR4TPgL/iGDbzqdTjOnWVQmqccRxDqtAZuJ27OG4rNmKFQHZ9SEJXQldkFNS8NvnE5uSt8ZHxtcVsVHJmkBeJC5lZNkjlkykEh166U8v6E1w7VnS2vzWSkWjkrgAW4DoJb+tiRRNSlRl8Vb7HJ9OtFN5cQKn35IzmnyL3XjL2HetciqDAO8PmJG7sxQhIWdS7PEut0snSz0KHVK1LDOLIQv7WQ8I4d+29LS2tYtCCfKZWOGxzWpuLGvdKWMYxWzlGu7L+PWwsXyS5TCshH2OM/uqHLyfBKSH5+nnBvbk8Bi9uX2eXp0sp8SngKHOuZMWwAlouaanSKNRyV5tqu0n4zWNhLDgIG7oj14xRAs/EtInNQ==~-1~-1~-1; bm_sv=AF6401A7B32DC54BED64C8AC150C5031~YAAQGy0+F94f+GaJAQAAwJ2xbBShrEf31fs4Mn0i4CYwIJQOXVRB4bTmfsxKNouPhxqJfBPTlYrncF+4moXHyacgWkoE+Cn4qB5yVDajNqjFLzGVROIQlZqRj5DIPHLL3ivw9X/xaon/tkU/cPSt3SlLQxMlUsZp06hW1OeVHVGmE78MOQPoxmh3XgVy5HRUk8fwQqNdg2Gh3LqgLPHp2+BsFZTrCkjsp6kA4BtejbXfbnnB4QPoNmlY5GgaQUnaEjlu~1; LPSID-31564604=1p68vDFDSeCxi80xPB-JiA; s_pers=%20productnum%3D3%7C1692321714565%3B%20s_nr365%3D1689746263831-Repeat%7C1721282263831%3B%20s_dslv%3D1689746263836%7C1784354263836%3B; s_sq=%5B%5BB%5D%5D; AMCV_F6421253512D2C100A490D45%40AdobeOrg=1585540135%7CMCMID%7C63435304895171780006669389195090073293%7CMCOPTOUT-1689753463s%7CNONE%7CvVersion%7C4.4.0",
    "Referer": "https://www.homedepot.com/",
    "Content-Length": "10380",
    "x-hd-dc": "origin",
    "apollographql-client-version": "0.0.0",
    "X-Api-Cookies": '{"x-user-id":"1c30d970-9527-b7c5-bea8-a52a5c833ccd"}',
    "X-current-url": "/p/HOMESTYLES-Dolly-Madison-White-Kitchen-Cart-with-Natural-Wood-Top-4511-95/207167048",
    "X-Experience-Name": "hd-home",
    "apollographql-client-name": "hd-home",
    "x-debug": "false"
}

response = requests.post("https://apionline.homedepot.com/federation-gateway/graphql?opname=reviews", headers=headers, data=data, verify=False, timeout=8)
# 解析响应数据
result = response.json()
print(result)
reviews = result['data']['reviews']['Results']