import requests
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
from note import Note


def upload_noteDday(titleraw,contentraw,price,rating,productname,img,groupid):
   
   note = Note()
   note.title_raw = titleraw
   note.content_raw = contentraw
   note.extend = price
   note.rate = rating
   note.product_name = productname
   note.files = img
   note.tag = '58,64,500'
   note.origin_files = img

   note.upload_new_note(note_group_id=groupid)
   

def get_json(id,idx,product_name = None,price=None,brand_name = None,groupid=None):

  '''
  id : String, eg: '2334231'
  idx: int,eg:1
  '''


  # 定义GraphQL查询
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

  # 请求头部
  headers = {
      "Accept": "*/*",
      "Accept-Language": "en-US,en;q=0.9",
      "Accept-Encoding": "gzip, deflate, br",
      "Host": "apionline.homedepot.com",
      "Origin": "https://www.homedepot.com",
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
      "Connection": "keep-alive",
      "Referer": "https://www.homedepot.com/",
      "Content-Length": "7109",
      # "x-hd-dc": "origin",
      # "apollographql-client-version": "0.0.0",
      # "X-Api-Cookies": '{"x-user-id":"3091817c-69d5-3846-7d61-1d1b0acef272"}',
      # "X-current-url": "/p/TITAN-Prestige-Series-Black-Faux-Leather-Reclining-3D-Massage-Chair-with-Bluetooth-Speakers-and-Heated-Seat-PRESTIGEBL/316140500",
      "X-Experience-Name": "hd-home",
      # "apollographql-client-name": "hd-home",
      # "x-debug": "false"
      # 添加其他所需的头部信息
  }

  # 请求体参数
  variables = {
      "filters": {
          "isVerifiedPurchase": False,
          "prosCons": None,
          "starRatings": None
      },
      "itemId": id,
      "pagesize": "10",
      "recfirstpage": "10",
      "searchTerm": None,
      "sortBy": "photoreview",
      "startIndex": idx
  }

  # 构建请求体
  data = {
      "operationName": "reviews",
      "variables": variables,
      "query": query
  }

  # 发送POST请求


  response = requests.post("https://apionline.homedepot.com/federation-gateway/graphql", headers=headers, json=data)

  # 解析响应数据
  result = response.json()



  reviews = result['data']['reviews']['Results']

  # 提取title、reviewtext和rating字段

  for single_reviewInfo in reviews:
    title = single_reviewInfo['Title']
    review_text = single_reviewInfo['ReviewText']
    rating = single_reviewInfo['Rating']
    img = single_reviewInfo['Photos']
    print('图片数量 ｜ ',len(img))



    all_img = ''
    if len(img) >1:
        
      for i in range(len(img)):
        single_img = img[i]['Sizes']['normal']['Url']
        print('图片',single_img)
        all_img = all_img+'___'+single_img
        all_img = all_img.strip()
      upload_noteDday(titleraw=title,contentraw=review_text,price=price,rating=rating,productname = product_name,img = all_img,groupid =groupid)
      print('上传成功')


    elif len(img) ==1:
       print(321)
       all_img = img[0]['Sizes']['normal']['Url']
       print('all',all_img)
       upload_noteDday(titleraw=title,contentraw=review_text,price=price,rating=rating,productname = product_name,img = all_img,groupid =groupid)
       print('上传成功')



    else:
       print('图片数量不达标，跳过')



  # 输出结果

def page_link(url,groupid=None):
   

  url = url
  headers = {
      # "scheme":"https",
      # "authority":"apionline.homedepot.com",
      # "path":"/federation-gateway/graphql?opname=searchModel",
      "Origin": "https://www.homedepot.com",
      "Content-Type":"application/json",
      "Connection":"keep-alive",
      'Cookie':'_abck=D1FEF740B7260868F97BDBFBD2398B71~0~YAAQDa08F9mjbCyJAQAA10eobArzOVcDh52Z9ewcoeg98e4lHZGVEs40D3DTNL3umgoBy9dg6qdqGxyRbOREGCO6b9MyqjnEy9SwwosAvsk3F23UXjDG6Fds0AJVDGdyK4Fh5UbjfFUzwZnJX0XDh+NX7L71MutyjLz2RdqMd4C/CfS2LU6GoH9RK/MgfPoYAnbO48JWc1nck48cOtuDZQA0V7fyoLZ8heA9JANm7/6jKujv0nzhExh7LxljP325AiIL+MNhTOGxKhkvPyqJFdAMc1X2QEa/ppCtF+/grJ+5wpbGdFTx9lRIu3kvG6dgaHHQnMl4uWIFME7VU8tqN7Mjl2t5NevYB/XpiP5QskAqlUhMq/zKFtzuYcHOYQj3HGU=~-1~-1~-1; s_pers=%20productnum%3D1%7C1692321577073%3B%20s_nr365%3D1689745115255-Repeat%7C1721281115255%3B%20s_dslv%3D1689745115256%7C1784353115256%3B; s_sess=%20s_pv_pName%3Dproductdetails%253E314372925%3B%20s_pv_pType%3Dpip%3B%20s_pv_cmpgn%3D%3B%20s_pv_pVer%3D%3B%20s_cc%3Dtrue%3B%20stsh%3D%3B; s_sq=%5B%5BB%5D%5D; RT="z=1&dm=www.homedepot.com&si=53696fb3-0ee9-4e13-97eb-588a00013570&ss=lk99o9hd&sl=2&tt=1xgs&rl=1&nu=1b78h28jt&cl=xtuv"; QuantumMetricSessionID=7412af5c7f5e9bbc3390db1264d54ec2; _pxde=da4d9aded4d4c26c9bf194223e17b9b180fb8577651f2094822db63f4453f8a1:eyJ0aW1lc3RhbXAiOjE2ODk3NDUxMTQ4NTcsImluY19pZCI6WyI2NWZjYWQ4OTcwNTkyMzk4Y2MzYjgzMmQyMTQzZTM5NiJdfQ==; LPSID-31564604=-on5lTlERNy0rgMD7f6aGg; LPVID=g5YjExYWIwODA4MmY1ZDUx; _px=ncInVKpUshGDsDCfT72XB8J5PN/A6bTDgkF4LNGICc9o5N7pVvNwsIi3e6H3DJFViwDb8hepGapKXj7s6e5EUA==:1000:TubfGh65eLoK3d8F59dIDwIesr/0dEn6n5W8LATcrPJfU+Er6sQNQLITAfrAydJ4iId5LPiLpdUMXxQFsuytNSAySTLW6Q0I2HVJc9Uxi137Ztbar4mYIsBWDfeRPJfHe1mQEv+9kr3oGgATf/1F1nX8Nd4/7zU53LTV6Is+a+Vp1LT+Ok+JyGcdPAIOhCFCVLdNbo5hHJ2VSfORzH9SnZax2Oj7blt8IuCJM1/LCL0v1kQydWFBOoBHB6KRtr6Hysg1iRh/cp2WJtaSrfHPRA==; aam_uuid=67110626292544481190565811597233401944; QuantumMetricUserID=788a48859efb2bdb56f2aa3f100b4cf2; ajs_anonymous_id=d582cb80-747a-47df-a05a-e3be7f4bee5e; _meta_adobe_aam_uuid=67110626292544481190565811597233401944; _meta_googleGtag_ga=GA1.2.1766730379.1684197508; _meta_metarouter_sessionID=1689743276270; _meta_metarouter_timezone_offset=-480; _meta_neustar_aam=67110626292544481190565811597233401944; _meta_neustar_mcvisid=67208209516724176660557732005229829677; trx=4708997196102404147; forterToken=56fbfd11b5dc4b70a2e300e38e94d64c_1689745094165__UDF43_13ck; mbox=PC#86e3d1df8ad445aab2bd6527b70fa645.34_0#1752989894|session#2d03e7426d3e4991856c8b2e8c729ceb#1689746954; IN_STORE_API_SESSION=TRUE; at_check=true; akavpau_prod=1689745391~id=7acc0473839afd1fd739cc3fdd5f99dd; QSI_HistorySession=https%3A%2F%2Fwww.homedepot.com%2Fp%2FTITAN-Prestige-Series-Black-Faux-Leather-Reclining-3D-Massage-Chair-with-Bluetooth-Speakers-and-Heated-Seat-PRESTIGEBL%2F316140500~1689743210219%7Chttps%3A%2F%2Fwww.homedepot.com%2Fb%2FSuper-Savings%2FN-5yc1vZ1z1phe1~1689743545003%7Chttps%3A%2F%2Fwww.homedepot.com%2Fp%2FLegend-Force-20-in-212-cc-Gas-Rear-Tine-Tiller-Forward-Reverse-LF20212RTG%2F314372925~1689744293377; THD_LOCALIZER=%257B%2522WORKFLOW%2522%253A%2522LOCALIZED_BY_STORE%2522%252C%2522THD_FORCE_LOC%2522%253A%25220%2522%252C%2522THD_INTERNAL%2522%253A%25220%2522%252C%2522THD_LOCSTORE%2522%253A%25226841%252BPatton%2520Twp%2520-%2520State%2520College%252C%2520PA%252B%2522%252C%2522THD_STRFINDERZIP%2522%253A%252216803%2522%252C%2522THD_STORE_HOURS%2522%253A%25221%253B8%253A00-20%253A00%253B2%253B6%253A00-22%253A00%253B3%253B6%253A00-22%253A00%253B4%253B6%253A00-22%253A00%253B5%253B6%253A00-22%253A00%253B6%253B6%253A00-22%253A00%253B7%253B6%253A00-22%253A00%2522%252C%2522THD_STORE_HOURS_EXPIRY%2522%253A1689747889%257D; AKA_A2=A; bm_sv=62B287DD7129BB0773E21CF81F992B53~YAAQLq08FxAi6S6JAQAA1DeMbBTh+jxXNWJiFFtzALuxFaGB1AHt0nMUC5la05Mx3LFoKdrfyBwhzybqFiMCBhGmXdLY1PjiCw5Wbzbj20+e0w08vnZJAFG8pTD7CNV4CRNH/a7wJrHTQth9LzmZL2HC6r3rM3WVWx+8ywFANDXpJBenv2VU6BngS/TN5Q9prhB4kEVgB3bt1/VDVEbQYBMnhuoUDrlCNXDqIkPVYzmpDy9g9ApR7BO7aGEJC+ygikYCEw==~1; _meta_mediaMath_iframe_counter=5; bm_sz=3F2430DF4E52D1FEFD1B251266000CA1~YAAQRK08FwEazFWJAQAAbVuCbBTSoqM8y3S3uznYR31hrrBzJ6b4DcCqJm7mEpb7qZfyPH1ynUWDuLN7WVmt2OkH3leoX0z0T7mzw2qmU53DpRfISPgwCY5MtOZinSoj8+o5eDgMeMhgYPCCbCL6SeM/TDAGOUG2QH12KPehdbebp1vO7P/2qU/jvOEfArNkzwLtoUEmqDQv/VJl5iNenNXv3I1vpGC8FVVMsRLMoiVDAQ9KeUCmLAxz5lp73bH4fwo9uwiEmI8ATuhjTU/M0vAm8+mbPYucmnf4AtjmRibBs3/GvnEXw/0Mx4ePOOmMbyoufgQq6+meXuz7kw8=~3424563~4473908; AMCV_F6421253512D2C100A490D45%40AdobeOrg=1585540135%7CMCMID%7C67208209516724176660557732005229829677%7CMCAAMLH-1690344912%7C9%7CMCAAMB-1690344912%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1689747312s%7CNONE%7CMCCIDH%7C1271793086%7CvVersion%7C4.4.0; ak_bmsc=E4BB643AD04EDE3B83C518A4BC23836F~000000000000000000000000000000~YAAQLa08F3NZBSeJAQAAU8RbbBQg6btrLbeu7SrJK2PKoFtDda2+iWGNQ7a0+xMMwPFVs3ta6hg2jiNO7C9sXFa+Lo906pLmbWdankJrIAVt8ZPRe7rc/3wG55G4hEpbBa8S4oj9sdewbBvis0wJzlaBhSdGWvPOhvfr50nS983kbwai8geoV2//picpyiKz7OTgJdyKkqvravI5darUGzuAZKlSjwKYnFl99BIDhL3bA5FbB+jqNkSG1uaDD7NcfBfzDiy83TLyp2CYS2x7LMmHF8OhW3+e0Pe4VJqXEAW1PLWPcKAJp9PrB6UifmORqrF5f52A3vJaBSwy8JW0lK99Kc5P8wCPUKnMA+J6zs4iOLwENqV2cx1ZM+HarEJyIif9aUBGNAhw1pg6JEzqleY3qWh8M6u1A/1rP6eewSpl/cLFDfWLyd4yT2SqefEvq3qDW/N1UJKwQsipIIMVTLEQ1Bqk4skxneJR8miWaBS+boe/O+dEBuCd; _meta_adobe_fire={"xandr":true,"revjet":true,"mediaMath":true}; _meta_adobe_google=1689729577200; _meta_adobe_microsoft=1689729577200; _meta_adobe_neustar=1689729577199; _ga_9H2R4ZXG4J=GS1.1.1689729454.2.1.1689729569.60.0.0; _ga=GA1.2.1766730379.1684197508; _gac_UA-32593878-1=1.1684197509.Cj0KCQjwsIejBhDOARIsANYqkD3GGgy2ylTLCqgrQToNFXCv3BrU23PAQiIdOv0nbsWe2Ac3AvNrIrsaAroJEALw_wcB; _gid=GA1.2.121220404.1689729455; _gcl_au=1.1.559171230.1684197509; _gcl_aw=GCL.1684197509.Cj0KCQjwsIejBhDOARIsANYqkD3GGgy2ylTLCqgrQToNFXCv3BrU23PAQiIdOv0nbsWe2Ac3AvNrIrsaAroJEALw_wcB; _gcl_dc=GCL.1684197509.Cj0KCQjwsIejBhDOARIsANYqkD3GGgy2ylTLCqgrQToNFXCv3BrU23PAQiIdOv0nbsWe2Ac3AvNrIrsaAroJEALw_wcB; _meta_inMarket_userNdat=BFB44F2D85D062642F1F575102AF5280; _meta_mediaMath_cid=6f3664b7-39ad-4c00-b943-8b433d32cc1e; _meta_mediaMath_mm_id=6f3664b7-39ad-4c00-b943-8b433d32cc1e; _meta_neustar_fabrickId=E1:oMjrOvIkMse3j722gUCFHaIGdstt4pv6DKkvO7kVaxnpsduwznA51VNxb5XB3OZuMpWyoQ-Ud_WXt3UeEcay_YuSXinXeF7q9e_mozX0iwo; _meta_neustar_tuid=204910904582000602982; _meta_amobee_uid=3167430014345719114; _meta_pinterest_derived_epik_failure=not found; _meta_pinterest_pin-unauth=dWlkPU1USTFPR1psT1RFdE5XRTRaQzAwWkRrNExXRmlZalF0WkRNeU5HVTBPRFptTUdJNA; _meta_tapAd_id=9c9e2135-78ef-4ca9-a420-976c2e509329; _meta_xandr_uid=0; _meta_xandr_uid2=uuid2=0; _meta_yahooMedia_yahoo_id_failure=timeout; thda.m=67208209516724176660557732005229829677; _meta_bing_beaconFired=1689729452766; _meta_facebookPixel_beaconFired=1689729452765; _meta_googleGtag_ga_library_loaded=1689729452769; _meta_movableInk_mi_u=d582cb80-747a-47df-a05a-e3be7f4bee5e; thda.s=415a6e4c-6260-bcf8-982b-4a668b8cde5d; _pxvid=f8b28924-f381-11ed-9d79-32bcaa56d69f; AMCVS_F6421253512D2C100A490D45%40AdobeOrg=1; THD_CACHE_NAV_SESSION=; THD_SESSION=; HD_DC=origin; THD_NR=1; akacd_usbeta=3867182241~rv=56~id=efb48ad4881ac0119c4ca66fac4e7ece; mp_0e3ea14e7e90fc91592bf29cb9917ec6_mixpanel=%7B%22distinct_id%22%3A%20%22188938be9cf23f7-09c505720813148-3c626b4b-1fa400-188938be9d02474%22%2C%22%24device_id%22%3A%20%22188938be9cf23f7-09c505720813148-3c626b4b-1fa400-188938be9d02474%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.homedepot.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.homedepot.com%22%7D; invoca_session=eyJ0dGwiOiIyMDIzLTA2LTA4VDAxOjUwOjA3LjYwMloiLCJzZXNzaW9uIjp7Imludm9jYV9pZCI6ImktNjc4NzAyNWQtOTIwZi00ODlmLTk1YzktYzdiNzM5ZWEyNDdlIn0sImNvbmZpZyI6eyJjZSI6dHJ1ZSwiZnYiOmZhbHNlLCJybiI6ZmFsc2V9fQ==; kampyleSessionPageCounter=1; kampyleUserSession=1686102602355; kampyleUserSessionsCount=1; kampyle_userid=f777-d46a-0558-44b4-d137-92ab-fb18-8af9; mdLogger=false; mp_a8adb55e36402861d6245b9451afd02c_mixpanel=%7B%22distinct_id%22%3A%20%22188938be9d31a23-0a7d5f7668b6948-3c626b4b-1fa400-188938be9d42a49%22%2C%22%24device_id%22%3A%20%22188938be9d31a23-0a7d5f7668b6948-3c626b4b-1fa400-188938be9d42a49%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.homedepot.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.homedepot.com%22%7D; QSI_SI_2lVW226zFt4dVJ3_intercept=true; DELIVERY_ZIP=16803; DELIVERY_ZIP_TYPE=AUTO; _meta_acuityAds_auid=780124595601; _meta_acuityAds_cauid=auid=780124595601; _meta_revjet_revjet_vid=4708997196102404147; _px_f394gi7Fvmc43dfg_user_id=ZjlkZjVmZDEtZjM4MS0xMWVkLTg5MzUtMTM0M2YzNDM0Zjhi; thda.u=3091817c-69d5-3846-7d61-1d1b0acef272; THD_CACHE_NAV_PERSIST=; THD_PERSIST=',

      "Referer":"https://www.homedepot.com/",
      "Content-Length": "10380",
      "x-hd-dc":"origin",
      "apollographql-client-version": "0.0.0",
      "X-Api-Cookies":'{"x-user-id":"3091817c-69d5-3846-7d61-1d1b0acef272"}',
      "X-current-url":"/p/TITAN-Prestige-Series-Black-Faux-Leather-Reclining-3D-Massage-Chair-with-Bluetooth-Speakers-and-Heated-Seat-PRESTIGEBL/316140500",
      "X-Experience-Name":"hd-home",
      "apollographql-client-name":"hd-home",
      "x-debug":"false"
  }
  


  data = '''
  {
      "operationName": "searchModel",
      "variables": {
          "storefilter": "ALL",
          "channel": "DESKTOP",
          "skipInstallServices": false,
          "skipKPF": false,
          "skipSpecificationGroup": false,
          "skipSubscribeAndSave": false,
          "additionalSearchParams": {
              "sponsored": true,
              "mcvisId": "67208209516724176660557732005229829677",
              "deliveryZip": "16803",
              "multiStoreIds": []
          },
          "filter": {},
          "navParam": "5yc1vZc3ovZ1z0kirf",
          "orderBy": {
              "field": "TOP_SELLERS",
              "order": "ASC"
          },
          "pageSize": 48,
          "startIndex": 0,
          "storeId": "6841"
      },
      "query": "query searchModel($keyword: String, $navParam: String, $storefilter: StoreFilter = ALL, $storeId: String, $itemIds: [String], $channel: Channel = DESKTOP, $additionalSearchParams: AdditionalParams, $loyaltyMembershipInput: LoyaltyMembershipInput, $startIndex: Int, $pageSize: Int, $orderBy: ProductSort, $filter: ProductFilter, $zipCode: String, $skipInstallServices: Boolean = true, $skipKPF: Boolean = false, $skipSpecificationGroup: Boolean = false, $skipSubscribeAndSave: Boolean = false) { searchModel(keyword: $keyword, navParam: $navParam, storefilter: $storefilter, storeId: $storeId, itemIds: $itemIds, channel: $channel, additionalSearchParams: $additionalSearchParams, loyaltyMembershipInput: $loyaltyMembershipInput) { metadata { hasPLPBanner categoryID analytics { semanticTokens dynamicLCA __typename } canonicalUrl searchRedirect clearAllRefinementsURL contentType h1Tag isStoreDisplay productCount { inStore __typename } stores { storeId storeName address { postalCode __typename } nearByStores { storeId storeName distance address { postalCode __typename } __typename } __typename } __typename } id searchReport { totalProducts didYouMean correctedKeyword keyword pageSize searchUrl sortBy sortOrder startIndex __typename } relatedResults { universalSearch { title __typename } relatedServices { label __typename } visualNavs { label imageId webUrl categoryId imageURL __typename } visualNavContainsEvents relatedKeywords { keyword __typename } __typename } products(startIndex: $startIndex, pageSize: $pageSize, orderBy: $orderBy, filter: $filter) { itemId dataSources identifiers { canonicalUrl brandName itemId productLabel modelNumber productType storeSkuNumber parentId isSuperSku __typename } media { images { url type subType sizes __typename } __typename } pricing(storeId: $storeId) { value alternatePriceDisplay alternate { bulk { pricePerUnit thresholdQuantity value __typename } unit { caseUnitOfMeasure unitsOriginalPrice unitsPerCase value __typename } __typename } original mapAboveOriginalPrice message preferredPriceFlag promotion { type description { shortDesc longDesc __typename } dollarOff percentageOff savingsCenter savingsCenterPromos specialBuySavings specialBuyDollarOff specialBuyPercentageOff dates { start end __typename } promotionTag __typename } specialBuy unitOfMeasure __typename } reviews { ratingsReviews { averageRating totalReviews __typename } __typename } availabilityType { discontinued type buyable status __typename } badges(storeId: $storeId) { name label __typename } details { collection { collectionId name url __typename } highlights installation { serviceType __typename } __typename } favoriteDetail { count __typename } fulfillment(storeId: $storeId, zipCode: $zipCode) { backordered backorderedShipDate bossExcludedShipStates excludedShipStates seasonStatusEligible fulfillmentOptions { type fulfillable services { type hasFreeShipping freeDeliveryThreshold locations { curbsidePickupFlag isBuyInStoreCheckNearBy distance inventory { isOutOfStock isInStock isLimitedQuantity isUnavailable quantity maxAllowedBopisQty minAllowedBopisQty __typename } isAnchor locationId storeName state type storePhone __typename } deliveryTimeline deliveryDates { startDate endDate __typename } deliveryCharge dynamicEta { hours minutes __typename } totalCharge __typename } __typename } anchorStoreStatus anchorStoreStatusType onlineStoreStatus onlineStoreStatusType __typename } info { hasSubscription isBuryProduct isSponsored isGenericProduct isLiveGoodsProduct sponsoredBeacon { onClickBeacon onViewBeacon __typename } sponsoredMetadata { campaignId placementId slotId __typename } globalCustomConfigurator { customExperience __typename } returnable hidePrice productSubType { name link __typename } categoryHierarchy samplesAvailable customerSignal { previouslyPurchased __typename } productDepartmentId productDepartment augmentedReality ecoRebate quantityLimit sskMin sskMax unitOfMeasureCoverage wasMaxPriceRange wasMinPriceRange swatches { isSelected itemId label swatchImgUrl url value __typename } totalNumberOfOptions paintBrand dotComColorEligible classNumber __typename } installServices(storeId: $storeId, zipCode: $zipCode) @skip(if: $skipInstallServices) { scheduleAMeasure @skip(if: $skipInstallServices) gccCarpetDesignAndOrderEligible @skip(if: $skipInstallServices) __typename } keyProductFeatures @skip(if: $skipKPF) { keyProductFeaturesItems { features { name refinementId refinementUrl value __typename } __typename } __typename } specificationGroup @skip(if: $skipSpecificationGroup) { specifications { specName specValue __typename } specTitle @skip(if: $skipSpecificationGroup) __typename } subscription @skip(if: $skipSubscribeAndSave) { defaultfrequency @skip(if: $skipSubscribeAndSave) discountPercentage @skip(if: $skipSubscribeAndSave) subscriptionEnabled @skip(if: $skipSubscribeAndSave) __typename } sizeAndFitDetail { attributeGroups { attributes { attributeName dimensions __typename } dimensionLabel productType __typename } __typename } dataSource __typename } taxonomy { brandLinkUrl breadCrumbs { browseUrl creativeIconUrl deselectUrl dimensionId dimensionName label refinementKey url __typename } __typename } templates partialTemplates dimensions { label refinements { refinementKey label recordCount selected imgUrl url nestedRefinements { label url recordCount refinementKey __typename } __typename } collapse dimensionId isVisualNav isVisualDimension isNumericFilter isColorSwatch nestedRefinementsLimit visualNavSequence __typename } orangeGraph { universalSearchArray { pods { title description imageUrl link __typename } info { title __typename } __typename } productTypes __typename } appliedDimensions { label refinements { label refinementKey url __typename } isNumericFilter __typename } __typename } }"
  }'''


  # startidx =48
  # for i in range(559):
  #   variables = {
  #       "startIndex": startidx
  #   }
  #   data_dict = json.loads(data)
  #   data_dict["variables"].update(variables)
  #   updated_data = json.dumps(data_dict)
  #   response = requests.post(url, headers=headers, data=updated_data)
  #   startidx += 1




  print(url)
  response = requests.post(url, headers=headers, data=data,timeout=8, verify=False)

  li = response.json()['data']['searchModel']['products']

  productlabel_li = product_li()



  for page_link_data in li:
    try:
      brand_name = page_link_data['identifiers']['brandName']

      productLabel = page_link_data['identifiers']['productLabel']

      print('获取产品信息 ｜ ',productLabel )


      if productLabel not in productlabel_li :
        log_scraped_product(productLabel)
        id=int(page_link_data['itemId'])
        price = page_link_data['pricing']['value']
        try:
          if page_link_data['reviews']['ratingsReviews']['totalReviews']:
            total_reviews = int(page_link_data['reviews']['ratingsReviews']['totalReviews'])
            print('total reviews | ',total_reviews)

            # url = page_link_data['info']['swatches'][0]['url']
            idx =1
            total_review_page = int(total_reviews // 10)

            if total_review_page > 1:


              for i in range(total_review_page):
                get_json(id,idx,brand_name=brand_name,product_name = productLabel,price = price,groupid=groupid)
                idx +=10
                print('下一页评论')
        except Exception as e:
           print('ERROR1',e)

      else:
        print('改商品已爬过，跳过')
          

    except Exception as e:
      print('Error',e)

     


def log_scraped_product(name):
  with open('name.txt', 'a') as f:
    f.write(name + '\n')

def product_li(filename='name.txt'):
    # Open the text file in read mode
    with open(filename, 'r') as file:

        # Read the lines of the file into a list
        lines = file.readlines()
        
        # Remove any newline characters from the end of each line
        lines = [line.strip() for line in lines]
    return lines






def get_itemidLink():


  headers = {
      # "Accept": "*/*",
      # "Accept-Language": "en-US,en;q=0.9",
      # "Accept-Encoding": "gzip, deflate, br",
      # "Host": "apionline.homedepot.com",
      # "Origin": "https://www.homedepot.com",
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
      # "Connection": "keep-alive",
      # "Referer": "https://www.homedepot.com/",
      # "Content-Length": "7109",
      # "x-hd-dc": "origin",
      # "apollographql-client-version": "0.0.0",
      # "X-Api-Cookies": '{"x-user-id":"3091817c-69d5-3846-7d61-1d1b0acef272"}',
      # "X-current-url": "/p/TITAN-Prestige-Series-Black-Faux-Leather-Reclining-3D-Massage-Chair-with-Bluetooth-Speakers-and-Heated-Seat-PRESTIGEBL/316140500",
      "X-Experience-Name": "hd-home",
      # "apollographql-client-name": "hd-home",
      # "x-debug": "false"
      # 添加其他所需的头部信息
  }
    # get the page source
    # 创建Chrome选项

  driver = webdriver.Chrome(executable_path='/Users/jianjunchen/Downloads/chromedriver_mac_arm64/chromedriver')
  driver.implicitly_wait(1.5)
  driver.get('https://www.homedepot.com/b/Furniture-Living-Room-Furniture/N-5yc1vZc7p3')


  
  # make sure we get all the links
  scroll_pause_time = 2 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
  screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
  i = 2
  
  # time.sleep(40)
  try:
      # scroll down to bottom
      while True:
          # scroll one screen height each time
          driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
          print('执行 ｜ 滑动当前商品浏览界面')  
          i += 1
          time.sleep(scroll_pause_time)
          # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
          scroll_height = driver.execute_script("return document.body.scrollHeight;")  
          # Break the loop when the height we need to scroll to is larger than the total scroll height

          if (screen_height) * i > scroll_height:
              break
  except ValueError:
      print("Error: Nothing to scrape")


  soup = BeautifulSoup(driver.page_source,'html.parser')

  ratings_count_element = soup.find_all(class_='ratings__count--6r7g3')
  for single_ratings_count_element  in ratings_count_element:
  
      ratings_count = single_ratings_count_element.get_text(strip=True)[1:-1]
      print('rate',ratings_count)


  # 找到所有包含链接的<a>标签
  # link_tags = soup.find_all('a')
  link_tags = soup.find('a', {'class': 'product-image'}).get('href')
  link_tags  = [a.get('href') for a in soup.find_all('a') if '/p/' in a.get('href')]
  # 提取链接
  all_pagelinks = []
  for link_tag in link_tags:
      print(link_tag)
      # link_tag = str(link_tag)
      # if '#ratings-and-reviews' in str(link_tag):
      #   link_tag = link_tag[:link_tag.index('#ratings-and-reviews')]
      #   print(link_tag)
      #   if link_tag not in all_pagelinks:
           
      #     all_pagelinks.append(link_tag)
           



  print(all_link)

  return all_pagelinks
def get_productlks(li):
    # 正则表达式模式
  pattern = r"^/p/.*\d$"

  # 提取符合条件的链接
  matched_links = [ link for link in li if re.match(pattern, str(link))]
  matched_links = list(set(matched_links))

  print('当页商品链接数量：',len(matched_links))
  return  matched_links
def id_list(li):
  pattern = r'/p/(\d+)/?$'

  numbers = []

  for link in li:
      print(link)
      match = re.search(pattern, link)
      if match:
          number = match.group(1)
          numbers.append(number)

  return numbers

if __name__ == '__main__':
  # all_link = get_itemidLink()
  # for i in all_link:
  #   print(i)

  try:
    url = 'https://apionline.homedepot.com/federation-gateway/graphql?opname=searchModel'
    page_link(url=url,groupid=1)

  except Exception as e:
    print('Final Error',e)
