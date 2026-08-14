#! /usr/bin/python
# coding: UTF-8
import sys
l1ll_opy_ = sys.version_info [0] == 2
l1lllll1_opy_ = 2048
l1l111l11_opy_ = 7
def l1l1ll1_opy_ (l1ll11l1l_opy_):
    global l1111_opy_
    l1l_opy_ = ord (l1ll11l1l_opy_ [-1])
    l1llllll_opy_ = l1ll11l1l_opy_ [:-1]
    l1l1111ll_opy_ = l1l_opy_ % len (l1llllll_opy_)
    l1l1l11_opy_ = l1llllll_opy_ [:l1l1111ll_opy_] + l1llllll_opy_ [l1l1111ll_opy_:]
    if l1ll_opy_:
        l1l111ll1_opy_ = unicode () .join ([unichr (ord (char) - l1lllll1_opy_ - (l11l1l1_opy_ + l1l_opy_) % l1l111l11_opy_) for l11l1l1_opy_, char in enumerate (l1l1l11_opy_)])
    else:
        l1l111ll1_opy_ = str () .join ([chr (ord (char) - l1lllll1_opy_ - (l11l1l1_opy_ + l1l_opy_) % l1l111l11_opy_) for l11l1l1_opy_, char in enumerate (l1l1l11_opy_)])
    return eval (l1l111ll1_opy_)
import sys
l1lll1l1l_opy_ = sys.version_info [0] == 2
l1l1lll1l_opy_ = 2048
l1ll1l1l1_opy_ = 7
def l1l1111ll_opy_ (l11lllll1_opy_):
    global l1ll11l1l_opy_
    l1l11l1l1_opy_ = ord (l11lllll1_opy_ [-1])
    l1l11l11l_opy_ = l11lllll1_opy_ [:-1]
    l1lll1l11_opy_ = l1l11l1l1_opy_ % len (l1l11l11l_opy_)
    l1l111l11_opy_ = l1l11l11l_opy_ [:l1lll1l11_opy_] + l1l11l11l_opy_ [l1lll1l11_opy_:]
    if l1lll1l1l_opy_:
        l1l11l111_opy_ = unicode () .join ([unichr (ord (char) - l1l1lll1l_opy_ - (l1ll1l111_opy_ + l1l11l1l1_opy_) % l1ll1l1l1_opy_) for l1ll1l111_opy_, char in enumerate (l1l111l11_opy_)])
    else:
        l1l11l111_opy_ = str () .join ([chr (ord (char) - l1l1lll1l_opy_ - (l1ll1l111_opy_ + l1l11l1l1_opy_) % l1ll1l1l1_opy_) for l1ll1l111_opy_, char in enumerate (l1l111l11_opy_)])
    return eval (l1l11l111_opy_)
import shutil
import codecs
import random
import importlib
import keyword
import errno
import sys
import os
import re
license = (
    l1l1ll1_opy_ (u"ࠨࠩࠪࡇࡴࡶࡹࡳ࡫ࡪ࡬ࡹࠦ࠲࠱࠳࠷࠰ࠥ࠸࠰࠲࠷࠯ࠤ࠷࠶࠱࠷࠮ࠣ࠶࠵࠷࠷࠭ࠢ࠵࠴࠶࠾ࠠࡋࡣࡦࡵࡺ࡫ࡳࠡࡦࡨࠤࡍࡵ࡯ࡨࡧ࠯ࠤࡌࡋࡁࡕࡇࡆࠤࡪࡴࡧࡪࡰࡨࡩࡷ࡯࡮ࡨ࠮ࠣࡻࡼࡽ࠮ࡨࡧࡤࡸࡪࡩ࠮ࡤࡱࡰࠑࠏࡒࡩࡤࡧࡱࡷࡪࡪࠠࡶࡰࡧࡩࡷࠦࡴࡩࡧࠣࡅࡵࡧࡣࡩࡧࠣࡐ࡮ࡩࡥ࡯ࡵࡨ࠰ࠥ࡜ࡥࡳࡵ࡬ࡳࡳࠦ࠲࠯࠲ࠣࠬࡹ࡮ࡥࠡࠤࡏ࡭ࡨ࡫࡮ࡴࡧࠥ࠭ࡀࠓࠊࡺࡱࡸࠤࡲࡧࡹࠡࡰࡲࡸࠥࡻࡳࡦࠢࡷ࡬࡮ࡹࠠࡧ࡫࡯ࡩࠥ࡫ࡸࡤࡧࡳࡸࠥ࡯࡮ࠡࡥࡲࡱࡵࡲࡩࡢࡰࡦࡩࠥࡽࡩࡵࡪࠣࡸ࡭࡫ࠠࡍ࡫ࡦࡩࡳࡹࡥ࠯ࠏࠍ࡝ࡴࡻࠠ࡮ࡣࡼࠤࡴࡨࡴࡢ࡫ࡱࠤࡦࠦࡣࡰࡲࡼࠤࡴ࡬ࠠࡵࡪࡨࠤࡑ࡯ࡣࡦࡰࡶࡩࠥࡧࡴࠎࠌࠣࠤࠥࠦࡨࡵࡶࡳ࠾࠴࠵ࡷࡸࡹ࠱ࡥࡵࡧࡣࡩࡧ࠱ࡳࡷ࡭࠯࡭࡫ࡦࡩࡳࡹࡥࡴ࠱ࡏࡍࡈࡋࡎࡔࡇ࠰࠶࠳࠶ࠍࠋࡗࡱࡰࡪࡹࡳࠡࡴࡨࡵࡺ࡯ࡲࡦࡦࠣࡦࡾࠦࡡࡱࡲ࡯࡭ࡨࡧࡢ࡭ࡧࠣࡰࡦࡽࠠࡰࡴࠣࡥ࡬ࡸࡥࡦࡦࠣࡸࡴࠦࡩ࡯ࠢࡺࡶ࡮ࡺࡩ࡯ࡩ࠯ࠤࡸࡵࡦࡵࡹࡤࡶࡪࠓࠊࡥ࡫ࡶࡸࡷ࡯ࡢࡶࡶࡨࡨࠥࡻ࡮ࡥࡧࡵࠤࡹ࡮ࡥࠡࡎ࡬ࡧࡪࡴࡳࡦࠢ࡬ࡷࠥࡪࡩࡴࡶࡵ࡭ࡧࡻࡴࡦࡦࠣࡳࡳࠦࡡ࡯ࠢࠥࡅࡘࠦࡉࡔࠤࠣࡆࡆ࡙ࡉࡔ࠮ࠐࠎ࡜ࡏࡔࡉࡑࡘࡘࠥ࡝ࡁࡓࡔࡄࡒ࡙ࡏࡅࡔࠢࡒࡖࠥࡉࡏࡏࡆࡌࡘࡎࡕࡎࡔࠢࡒࡊࠥࡇࡎ࡚ࠢࡎࡍࡓࡊࠬࠡࡧ࡬ࡸ࡭࡫ࡲࠡࡧࡻࡴࡷ࡫ࡳࡴࠢࡲࡶࠥ࡯࡭ࡱ࡮࡬ࡩࡩ࠴ࠍࠋࡕࡨࡩࠥࡺࡨࡦࠢࡏ࡭ࡨ࡫࡮ࡴࡧࠣࡪࡴࡸࠠࡵࡪࡨࠤࡸࡶࡥࡤ࡫ࡩ࡭ࡨࠦ࡬ࡢࡰࡪࡹࡦ࡭ࡥࠡࡩࡲࡺࡪࡸ࡮ࡪࡰࡪࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴࠢࡤࡲࡩࠓࠊ࡭࡫ࡰ࡭ࡹࡧࡴࡪࡱࡱࡷࠥࡻ࡮ࡥࡧࡵࠤࡹ࡮ࡥࠡࡎ࡬ࡧࡪࡴࡳࡦ࠰ࠪࠫࠬࠒ")
)
# =========== l1l1ll11l_opy_ constants
l1l1l1lll_opy_ = sys.version_info[0] == 2
if l1l1l1lll_opy_:
    import __builtin__ as l1l1ll11l_opy_
else:
    import builtins as l1l1ll11l_opy_
l1l111111_opy_ = l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡷࠥုၹၼၹဩတࠥࠓ"))
l1lll11ll_opy_ = l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡸࠦေွီဳဲး၁ေပࠢࠔ"))
random.seed()
l1l1l1lll_opy_ = 2048
l1l11l1l1_opy_ = l1l1l1lll_opy_
l1l11lll1_opy_ = 7
print(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡹࠧဳၻၿဤီၜၗဵဠ၅ၳၴၮၳၳၵၴၥၨၴၯာ၍ၷၰၺၱဪၙၯၦၹၲၭဪၜၹၶၬၵၶဪၛၢၨၹၹၫၫႀၯၴဤၜၭၼၿၩၱၲဦႃႇဳတࠣࠕ")).format(
    l1l111111_opy_.capitalize(), l1lll11ll_opy_))
print(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡺࠨဧ၅ၳၶႁၼၵၧၪၸဦူ၍ဵဠ၉ၩၧၼၯၯဠ၇ၲၭၱၸၱၥၴၭၴၯးာ၌ၫၧၫၶၽၱ်ဢ၅ၶၩၭၴၥဢံဴးဪၭၴဢဤၮၼၾၼ်ေဳၽၿႁ်ၡၲၥၩၰၯ်ၯၴၫဵၴၳၯၥၰၷၫၻ္ၘ၉၅၉ၔၛ၏္ဲူဴၢၶေဗࠢࠖ")))
def main():
    global l1l11llll_opy_
    global l1l11l1l1_opy_
    global l1lll111l_opy_
    global l1l1lll1l_opy_
    def l1l1l1ll1_opy_(l1lll11l1_opy_, open=False):
        try:
            os.makedirs(l1lll11l1_opy_.rsplit(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡻࠢဩဳိဖࠧࠗ")), 1)[0])
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        if open:
            return codecs.open(l1lll11l1_opy_, encoding=l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡵࠣါၻၼၰ္းဩပࠥ࠘")), mode=l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡶࠤိၿေယࠢ࠙")))
    def l1ll1111l_opy_(l1lll1ll1_opy_, name):
        return l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡷࠥုႅြၽၽဵႃႃြႉဧဖࠤࠚ")).format(
            l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡸࠦေၫၟဩဘࠥࠛ")) if name.startswith(
                l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡹࠧဳၟၡါယࠦࠜ"))) else l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡺࠨဧၡါရࠦࠝ")) if name.startswith(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡻࠢဩၣိဝࠧࠞ"))) else l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡵࠣါၲုဟࠨࠟ")),
            bin(l1lll1ll1_opy_)[2:] .replace(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡶࠤိးေအࠢࠠ")), l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡷࠥုၶဳလࠣࠡ"))),
            l1l1111l1_opy_
        )
    def scramble(l1l11l111_opy_):
        global l1l11l1l1_opy_
        if l1l1l1lll_opy_:
            l1l111l11_opy_ = unicode() .join([unichr(l1l1l1lll_opy_ + ord(char) + (
                l1ll1l111_opy_ + l1l11l1l1_opy_) % l1l11lll1_opy_) for l1ll1l111_opy_, char in enumerate(l1l11l111_opy_)])
            l1l11ll1l_opy_ = unichr(l1l11l1l1_opy_)
        else:
            l1l111l11_opy_ = str() .join([chr(l1l1l1lll_opy_ + ord(char) + (
                l1ll1l111_opy_ + l1l11l1l1_opy_) % l1l11lll1_opy_) for l1ll1l111_opy_, char in enumerate(l1l11l111_opy_)])
            l1l11ll1l_opy_ = chr(l1l11l1l1_opy_)
        l1lll1l11_opy_ = l1l11l1l1_opy_ % len(l1l11l111_opy_)
        l1l11l11l_opy_ = l1l111l11_opy_[:-
                                                    l1lll1l11_opy_] + l1l111l11_opy_[-l1lll1l11_opy_:]
        l11lllll1_opy_ = l1l11l11l_opy_ + l1l11ll1l_opy_
        l1l11l1l1_opy_ += 1
        return l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡸࠦေႁဢဩဟࠥࠢ")) + l11lllll1_opy_ + l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡹࠧဳဢဩဠࠥࠣ"))
    def l1ll1l11l_opy_(l1ll1ll1l_opy_):
        return l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡺࠨဧဩါဓဒၳၹၰၱၶၺဨၽႅၳဏဎဓဒၳၿၐၻၸၮၷၸှၻဲႁဦ၅ဪၿၹၵဲၼၭၼၿၩၱၲၥၱၸၲၯဢၟံၥဪ၉ွဢံဓဒၭၴၡၴ၆ၧၻၯႇူၿဤ၃ဨႅွၽဏဎၩၰၫၾ၍ၱၨၻၴၿၿၻဲႁဦ၅ဪႇဲၿထတပနၰၥၨဤၻၶၝၯၲၣၱၨၴၯႇူၿဤီၳၯႅၥၦၗၺၺၳၺၧ၎ၭၺၭၼၭၬါှဓဒဪာဠဢၫၲၷၬၭၬဢၷၺၺၳၺၧၐၶႁးႇမညဢဤဦဨဗဖဠဢဤဦၻၾၾၩၰၫၔၺဪ၉ဠၱၶၪဨဲၷၥၻၩၪၛၾၾၩၰၫၒၱၾၱၲၣၰဦၣ့ွၝါထတဨဪာဠၴၳၺၩၾၱၤၕၸၸၱၸၳ၌ၫၸၫၺၫၸဠဿဤၱၭႃၱၤၕၸၸၱၸၳ၌ၫၸၫၺၫၸဠၝှဳ္ၧမညဢဤဦဨဗဖဠဢဤဦၺၹႀၡၶၭၵၶ၎ၵၳၶၥၴၫၯာွဢၷၺၺၳၺၧၐၶဦိဪၸၥၰဤီၺၹႀၡၶၩၪၛၾၾၩၰၫၒၱၾၱၲၣၰုပနာဠဢဤၸၭၭၻၤၧၨၙၼၼၵၮၩၐၯၼၯၾၡၮဤ၃ဨၼၻၴၣၸၫၬၝႀၲၫၲၭၔၳႀၥၴၥၲဨၥ၆ၲၱၸၧၼၳၻၮ၆ၭၹၼၫၺၣၧၡဦဳဪၾၯၶၥၺၭၮၟၴၴၭၴၯၖၵၴၧၶၧၴဪၧၲၱၸၧၼၳၻၮ၆ၭၹၼၫၺၣၧှၣပနာဠဢဤဦဨဪာဍဌဤဦဨဪၵၦဢၭၹၘႃႀၨၱၲးႃ်ႉ်ဏဎဦဨဪာဠဢဤဦၻၾၾၩၰၫၒၱၾၱၲၣၰဦ၅ဪႁၮၫၧၵၬၯာဨါဤဴၲၹၵၮဢာၡၽၸၵၣၪၶဦူၹၾၤဢာၩၰၫၾဩဢေဦၫၲၭၲ၄ၥၹၭႅြၽဢေဦူၭၴၡၴ၍ၴၬၯႄဠိဤၹၼၼၵၮၩၒၸေဪေဠၥၬၧၺၗၻၤၷၰၻၻႅြၽါဤၬၷၼာၣၪၥၸၑၸၰၥၺူဦၫၲၭၲဢၭၴဨၯၺၵၯၩၸၩၾၱဠဪၶၫၫၹၰၥၦၗၺၺၳၺၧ၎ၭၺၭၼၭၬါၡုပနာဠဢဤၫၴၽၱ်ဏဎဦဨဪာဠဢဤဦၻၾၾၩၰၫၒၱၾၱၲၣၰဦ၅ဪၿၴၴဤီေဪ်ၪၱၭၴဨဲၧၣၪၶဦူၹၾၤဢာၩၰၫၾဩဢေဦၫၲၭၲ၄ၥၹၭႅြၽဢေဦူၭၴၡၴ၍ၴၬၯႄဠိဤၹၼၼၵၮၩၒၸေဪေဠၥၬၧၺၗၻၤၷၰၻၻႅြၽါဤၬၷၼာၣၪၥၸၑၸၰၥၺူဦၫၲၭၲဢၭၴဨၯၺၵၯၩၸၩၾၱဠဪၶၫၫၹၰၥၦၗၺၺၳၺၧ၎ၭၺၭၼၭၬါၡုပနာဠဢဤဦဨဪာဍဌဤဦဨဪၾၥၶၹၸၶဪၱၶၣၰဦူၽႀၲၫၲၭၔၳႀၥၴၥၲေဗဖဠဢဤဦုေဳဟࠣࠤ")).format(l1l1l1111_opy_, l1l1l1lll_opy_, l1l11lll1_opy_)
    def l1111l1l_opy_(l1l1ll1ll_opy_):
        print(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡻࠢၴါိုဗဖွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿထတႃ်ႉဠၹၭၲၴဪၻၢၨၹၹၫၫႀၥဢၽၵၽၼာၥၺၸၫၶၽၵၶၧူဦၺၯၭၬဢၻၵၺၶၰာဢၱၻၴၾၵဠၯၳၪၽၶၱဠၒၽၺၰၹၺဠၵၳၻၺၭၱဠၥၳၪၭဪၲၯၴဤၬၺၯၱအဏဎ၇ၶၮာၙၑၙဦၫၲၻၯၵၩဦၸၯၾဠၲၶၵၲၯၯၴဢၻၮၩၾာၴၱဤၵၪၰႁၳၥၥၺၭဪၭၮၦဤၽၰၫႀဠၰၳၺဴဪၮၹဢၩၪၱၾႀၩၰၫဦၼၲၱဠၥၳၴၮၳၳဠၨၭၲၭးမညဏဎဳဨ၌၍၃၍ၙၖဨၣၛၕၔဤ၉ၗ၎ၑဠ၃ၒ၊ဨၠ၍၌ၗ၅၈ၔ၏ာ၄၃ၘ၇ဨၞၛဠ၃ၒဦၗၐၒိ၎၍ၔ၍ဪၙ၅၆၍ၛၕဪၒ၉ၔၗၚဨၞၛဠၒၖ။ၞ၏ၚၔဢ၅၉။ၓၐ၅ၐၘ၇ၔဪၘ၏ၕၗဦၗၐာၗၑၖၑဩါိဍဌၘၮၭၸာၣၱၴၿဨၾၴၥဢၨၫၮၫႁၬၶဤၩၷၸၲၩၩဤၬၱၶၱဠၶၳဦၼၲၱဠၵၳၻၺၭၱဠၶၳၶဨၮၵၲၧၧၺၷၼႅဠှၸၵၸၮၵၲ၀ဤၧၶၮာၲၷၲဦႃ်ႉဠၨၶၵၵဪႀၨၧၶၫံဗဖ၉ၶဤၽၱၶၸဠၩၩၴၭၼၭၴၧဤၧၶဪၻၢၨၹၹၫၫႀၩၱၲဦၬၳၾၥၥၸၵၺႃာြၶၳၶၬၳၾှေဲဴ့၆ႀၯၲၨၯၺ၈ၫၻဳႁဓဒဗဖိဢ၅ၺဨၰၵၲၵၸဦၻၹၹၥဢၭၪၭၸႀၩၨၭၫၺၽာၭၣၽဦၪၯာၯၤၪၻၻၭၭၴၧၨဦၼၲၭၴဢၷၮၷၿၸၤၰါၺဨၬၱာဢၩဴၯးာၳၱၱၫဨၹၲဠၶၬၵၻၯာၩၯၴၵၺၾၱၤဢၪၸၷၷာၥၺၸၫၺၸၭၬဢၱၵၬၿၸၥၵဲဓဒ။ၰၡၲၸဦႁၹႁၲဢၧၵၶၰၵၧဢၪၯၴၯာၴၱဤၧၾၹၵၤဢၸၮၱၽးဠၧဲၭံဪၮၹဢၥၪၬၳၺၧဢၩၾၼၯၾၮၣၰဦၵၹၰၵၮၩဦၶၫၹၥၵဤၺၰၫႀဠၹၭၲၴဪၮၥဢၶၫၫၿၾၳၫၺၫၴႃာၳၥၥၴၶၯၰဠၨၳၸဨၳၰၥၰၸၯၮၳၱၲၵဲဓဒၣၻၵဢၱၧႁဪၭၬၵၳဦၭႂၯၬၷၨၫဨၭၱၲၶၥၯၶဪႃၯၴၨၹဨၹၾဠၨၭၲၭၽာၩၰဤၿၷၿၾဠၲၶၵၲၯၯၴဢၪၸၷၷာၯၤၪၻၻၭၭၴၫၳၴဨၯႄၰၮၭၩၱၾၸၹူထတပန္ဠၕၳၻၺၭၱဠၦၭၸၭၭႀၯၴၽဲဨၹၮၦၷၷၩၩၾၵၯၰဤၪၱၼၱၣၶၳၸႁဪၭၮၦဤၩၷၸၲၩၩဤၬၱၶၱဠၲၥၺၰဪၯၡၰဤၧၴၽၻဠၤၩဦၻၿၼၰၮၭၫၬဪၭၳဢၧၵၵၷၭၮၦဤၲၱၸၱဠၲၥၸၩၷၱၴၧၶၹံဗဖၔၪၩဦၫၹၺၦၫၫဦၮၳၸၥဢၴၧၼၲာၳၪၳၻၴၮာၢၧဤၹၷၷၱၴၪၭၴၯဪၸၩၭၩဦ။၄ျၣၱၲၬၱၱၫၦၫၰၫၻ္ၻၰၻဲၩၶၰးဠၵၳဦၱၸၯၬၷၨၯၶၱာၴၪၩဦၮၳၸၥဢၲၧၵၯာၡၰၨဦၭႂႀၥၰၷၯၷၸ်ဍဌၳၶႁဪၧြၵၳၻၺၭၱဠၦၭၸၭၭႀၯၴၽ၄ဨၥ၈ၴၣၶၭၭၾာၤၫၶၫၫၾၻၲၻ၂ဦၣ၆ၯၯၰၪၯၯဪၲၩၮၩဦၸၫႀၨ၀ၡၣၥဗဖဍဌေဦ။ၹၹၭၧၲၺၻဪၭၮၦဤၹၼၼၵၮၩဤၲၱၾၱၲၣၰၹဨၭၭၮဢၦၫဨၷၭၲၭၩၪဨၫၿဠၲၰၧၱၸးဠၤၽၶၩၽၿၩၰၫဦၷၬၲၵၵၧၧၼၳၻၮဏဎ၈ၭဪၿၵၴၩဦၼၹာၴၣၯၫဨၫာၬၱၳၱဨၫႀဠၶၬၫဨၭၻၭၯၩၴၼၽာၩၰဤၺၰၯာၣၱၲၬၱၱာၦၫၰၫဨၹၼၹၡၧၵၶၰၵၧူၸၾၼဪႀၯဢၨၯၻၭၻၶၧၶဦၩၶၸဠၨၩၧၼၿၾၥၵဲဓဒဗဖ။ၰၳၽၶဪၸၩၯၭၺၩၾၵၯၰၷ၀ပနမညုဤ၇ဨၭၻၭၯၩၴၼဪၭၦၶၩၸဨၫာၳၶၶၯၶၱာၬၫၸၫၺၫၸဠၵၬၵၽၶၰဠၤၩဦၸၼၱၣၧၨၫၬဪၮၹဢၻၮၱၾၱၳၲၥၩၭဗဖိဢ၅ဦုဪၻၲဢဦဦၱၸၿၩၦၩဦၩဪၿၴၴၭၴၯဪၸၩၶၩၸၩၶာၳၪၳၻၴၮာၢၧဤၫၻၭၭၰၧၨဦၿၳႀၨဢၠဦၺၫႀၨၧၶဦၼၲၱၮဢၨၵၽၬၸၥၦထတဵဪၕၦဢၸၮၭဪၼၥၲြၥၫၹၹၭၧၲၺၻဪၻၰၶၭၵၶဪၵၳဢ၊ၧၴၽၱဠဪၸၮၭဪၰၥၨၥၻၴၾဵာဢၥဦႃြႉဠၫၲဦၩဪၿၴၴၭၴၯဪၸၩၶၩၸၩၶာၣၣၲဦၷၸၸၹဢၦၫဨၿၿၥၦဤၧၼဪႀၨၧဤၹၼၫၾၴီဤၹၷဪႁၳၧဤိၸေဳၻဴႁိုၼဳဠၴၥၺၰၯၾဠၶၬၧၶဪဳၰၽံႃၺေမညုဤ၏ၮဪႀၨၧဤၶၭၺ၄ၟၥၳၳၵၯၺၴၵဤၵၸၾၵၯၰဤၯၻဪၿၥၶဤၺၷဪၠၲၷၩဲဨၲၻၷၧၺၫၺံာၯၰၰၿဨၫာြၤၰၧၶၵ၊ြၤၰၧၶၵ၊ၻဴႁ၂ၪၶၭၮၭ၂ဦၫၫၺၮၱၸဦၪၯာၵၵၩၪဨၳၺဠၶၬၫဨၷၵၤၦၰၫဨၹၾဠၣၸဦၼၲၱဠၧၲၪဨၹၲဠၣဤၹၼၼၵၮၩဤၲၱၾၱၲၣၰဓဒ့ာ၏ၤၪၻၻၭၭၴၫၳၴဨၹၲဠၵၸၸၱၸၳဠၮၭၺၭၼၭၬၵဤၯၻဪႁၮၵၹၯၼၫၮၬၧဤၬၷၼာၳၧၲၹၱၾၵၶၧဤၯၶၰၻၲၯၥၺၱၹၺဠၵၭၴၫၯာၩၶဤၩၩၸာၢၧဤၺၺၳႂၩၣၰၲႁဪၮၲၱၯၫၶဗဖိဢၒၵဨၼၱၮၣၱၯၶၱာၢၣၧၱၬၹၻၲဢၷၻၸၺၻၲၶဤၬၷၼာၭၧၸၮၷၮၿဠၵၸၧၺၾၵၮၩဤၽၱၾၴဠၡၣဦူၸၻၮုၳၼၭၼၾၩၦၥၨၴၯာၭၧၸၮၷၮၿာဢၥၲၻၹာၫၰၳၽၶဪၭၳဢၴၸၱႀၭၴၧဤၳၭၾၴၯၦၷုပနမည၎ၭၩၭၸၯၥြထတႃွႉဍဌ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃၅၇၉ွဿ၁၃ပနမညဢဤဦဨဪာဠဢါိုဥࠨࠥ")).format(l1l111111_opy_.capitalize(), l1l111111_opy_, l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡵࠣၶိါေဧࠢࠦ")), license))
        exit(l1l1ll1ll_opy_)
    if len(sys.argv) > 1:
        for l1l1111l1_opy_ in l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡶࠤိ၇ေဨࠢࠧ")), l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡷࠥု့ၴဧဤࠤࠨ")), l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡸࠦေ္ိၪၩၲၸေဪࠢࠩ")):
            if l1l1111l1_opy_ in sys.argv[1]:
                l1111l1l_opy_(0)
        l1l1ll11l_opy_ = sys.argv[1] .replace(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡹࠧဳၜၞါဨࠦࠪ")), l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡺࠨဧေါဩࠦࠫ")))
    else:
        l1l1ll11l_opy_ = os.getcwd() .replace(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡻࠢဩၠၢုာࠨࠬ")), l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡵࠣါဵုိࠨ࠭")))
    if len(sys.argv) > 2:
        l1l11111l_opy_ = sys.argv[2] .replace(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡶࠤိၤၦဳဩࠣ࠮")), l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡷࠥု္ဳဪࠣ࠯")))
    else:
        l1l11111l_opy_ = l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡸࠦေႇူၿဳႁ္ႇၫၻဴႁိုࠧ࠰")).format(
            * (l1l1ll11l_opy_.rsplit(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡹࠧဳုဩီࠥ࠱")), 1) + [l1l111111_opy_]))
    if len(sys.argv) > 3:
        l1l1l1ll1_opy_ = sys.argv[3] .replace(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡺࠨဧၞၠိေࠧ࠲")), l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡻࠢဩဳိဲࠧ࠳")))
    else:
        l1l1l1ll1_opy_ = l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡵࠣါႁးႇျၻဳႁၥၫၹၺၦၫၫဴၼႂႀဧူࠤ࠴")).format(
            l1l1ll11l_opy_, l1l111111_opy_)
    try:
        l1l1l1l1l_opy_ = open(l1l1l1ll1_opy_)
    except Exception as exception:
        print(exception)
        l1111l1l_opy_(1)
    exec(l1l1l1l1l_opy_.read(), globals(), locals())
    l1l1l1l1l_opy_.close()
    l1lll111l_opy_ = locals()
    def l111lll1_opy_(l1l111ll1_opy_, default):
        try:
            return l1lll111l_opy_[l1l111ll1_opy_]
        except:
            return default
    l1111111_opy_ = l111lll1_opy_(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡶࠤိၷၬၲၵၵၧၧၼၯၫၳၶၶၯၶၱၿဧေࠤ࠵")), False)
    l1111l1l_opy_ = l111lll1_opy_(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡷࠥုၫၿၣၫၭၥၻၾၾၩၰၫၹုံࠨ࠶")), False)
    l1l1111l1_opy_ = l111lll1_opy_(
        l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡸࠦေၻၢၨၹၹၫၫႀၥၦၣၴၩၷၱၟၶၥၯၴေးࠢ࠷")), l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡹࠧဳၟၽႁၥုးࠨ࠸")).format(l1l111111_opy_))
    l1l1l1111_opy_ = l111lll1_opy_(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡺࠨဧၲၰၧၱၸၫၭၣၶၱၭၼဳဴࠣ࠹")), l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡻࠢဩၣႁႅၩဳဵࠣ࠺")).format(l1l111111_opy_))
    l1lll11ll_opy_ = l111lll1_opy_(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡵࠣါၶၭၺ၄ၟၥၳၳၵၯၺၴၵါ္ࠦ࠻")), True)
    l1l1ll11l_opy_ = l111lll1_opy_(
        l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡶࠤိၻၹႁၲၥၩၥၭႂႀၥၰၷၯၷၸၿဧးࠤ࠼")), l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡷࠥုၺႅဠၲၽၾုွࠨ࠽"))) .split()
    l1l1l1l1l_opy_ = l111lll1_opy_(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡸࠦေၿၫၫၴၥၭႂႀၥၰၷၯၷၸၿဧ်ࠤ࠾")), l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡹࠧဳၰၻၧိှࠧ࠿"))) .split()
    l11l1111_opy_ = l111lll1_opy_(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡺࠨဧၵၯၯၸၩၼၡၶၬၥၮၼၭၧၯၩၴၼၽဳျࠣࡀ")), l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡻࠢဩါဿࠦࡁ"))) .split()
    l1l1l1ll1_opy_ = l111lll1_opy_(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡵࠣါၫႀၾၱၲၰၥၲၧၷၻၤၷၰၫၻေ၃ࠢࡂ")), l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡶࠤို၃ࠨࡃ"))) .split()
    l1l11l11l_opy_ = l111lll1_opy_(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡷࠥုၺၸၡၫၲၥၮၳၸၥၵါ၂ࠦࡄ")), l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡸࠦေဳ၀ࠣࡅ"))) .split()
    l1ll11l1l_opy_ = l111lll1_opy_(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡹࠧဳၰၮၥၯၶၩၺၡၯၩၹု၆ࠨࡆ")), l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡺࠨဧဩ၄ࠥࡇ"))) .split()
    l1l1ll1l1_opy_ = [
        l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡻࠢဩၿံႅ္ႇေၿါ၆ࠦࡈ")).format(directory.replace(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡵࠣါၢၤေ၊ࠢࡉ")), l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡶࠤိ့ေ။ࠢࡊ"))), l1llll1ll_opy_)
        for directory, l1lll1l11_opy_, l1lll1111_opy_ in os.walk(l1l1ll11l_opy_)
        for l1llll1ll_opy_ in l1lll1111_opy_
    ]
    def l11ll111_opy_(l1l1l11ll_opy_):
        for l1ll111l1_opy_ in l11l1111_opy_:
            if l1ll111l1_opy_ in l1l1l11ll_opy_:
                return True
        return False
    l1l1ll1ll_opy_ = [
        l1l1l11ll_opy_ for l1l1l11ll_opy_ in l1l1ll1l1_opy_ if not l11ll111_opy_(l1l1l11ll_opy_)]
    l111ll1l_opy_ = re.compile(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡷࠥၺေၪၻဲႁဧု။ࠨࡋ")).format(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡸࠦၼဳဣဩ၉ࠥࡌ"))))
    l1l11l11l_opy_ = re.compile(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡹࠧဳၣၱၨၯၶၱၧ်ဿၡၢၻဴဴၛုၠၽံၧ့ဩဩ၊ࠥࡍ")))
    l11llll11_opy_ = re.compile(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡺࠨဧူီႁးႇ်ဪဩ။ࠥࡎ")).format(l1l1l1111_opy_), re.DOTALL)
    def l1l111111_opy_(l1l111l1l_opy_):
        comment = l1l111l1l_opy_.group(0)
        if l11llll11_opy_.search(comment):
            l1l11ll1l_opy_.append(comment.replace(l1l1l1111_opy_, l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡻࠢဩါ၍ࠦࡏ"))))
            return l1l11ll11_opy_
        else:
            return l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡵࠣါိ၏ࠧࡐ"))
    def l1l1l1lll_opy_(l1l111l1l_opy_):
        global l1lll111l_opy_
        l1lll111l_opy_ += 1
        return l1l11ll1l_opy_[l1lll111l_opy_]
    l1l1l1lll_opy_ = (
        re.compile(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡶࠤၸုႅြၽၽဵႃႃြႉီာ၃ဪုၑࠨࡑ")).format(
            l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡷࠥၺာဴဿှဥိောၓࠢࡒ")),
            l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡸࠦၼဳဨ၁၀ဧဪဳဳ၎ࠣࡓ")),
            l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡹࠧၾဧဢဤဩဨေၕࠢࡔ"))
        ), re.MULTILINE)
        if l1lll11ll_opy_ else
        re.compile(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡺࠨၲဩၿံႅႅွၽၽံႃံဴ။ဤဩၒࠥࡕ")).format(
            l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡻࠢၴဦီ၇၆ိဧါဦၔࠦࡖ")),
            l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡵࠣၶိူ၉၈အဤိိၖࠧࡗ")),
            l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡶࠤၸုိဳၓࠣࡘ"))
        ), re.MULTILINE)
    )
    l1l11ll11_opy_ = l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡷࠥုၩႇူၿၣၩၧေၚ࡙ࠢ")).format(l1l111111_opy_)
    l111l11l_opy_ = re.compile(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡸࠦၼဳၻဲႁိၙ࡚ࠧ")).format(l1l11ll11_opy_))
    l1ll1l11l_opy_ = re.compile(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡹࠧၾဧူီႁးႇ်ဪဩၘ࡛ࠥ")).format(l1l1l1111_opy_))
    def l1l1l11l_opy_(l1l111l1l_opy_):
        string = l1l111l1l_opy_.group(0)
        if l1111111_opy_:
            if l1ll1l11l_opy_.search(string):
                l1lll1ll1_opy_.append(string.replace(l1l1l1111_opy_, l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡺࠨဧဩၙࠥ࡜"))))
                return l11llllll_opy_
            else:
                l1lll1ll1_opy_.append(scramble(string))
                return l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡻࠢဩၹၴၛၭၾၡၯၦၲၭႅြၽဢာႁ္ႇဵဧၙࠤ࡝")).format(l1l1l1111_opy_, l11llllll_opy_)
        else:
            l1lll1ll1_opy_.append(string)
            return l11llllll_opy_
    def l1l1ll1l1_opy_(l1l111l1l_opy_):
        global l1l11llll_opy_
        l1l11llll_opy_ += 1
        return l1lll1ll1_opy_[l1l11llll_opy_]
    l1l111l1_opy_ = re.compile(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡵࠣၶိူၥၾၵၟႀၸၽႆႁၲါ၃ီူႅြၽါႀီႃျႉဩၾာႁ်ႇဵၼဪၿ္ႅဳဵဧၚࠤ࡞")).format(
        l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡶࠤၸဪေဳဧူီ၅ူ၉၈အၝၢၢၤၧၨၜါာ၅၄ါၧၞၞၠၣၤေဵဧဩါဨၞࠧ࡟")),
        l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡷࠥၺေီဢဤဲူ၇ဲ။ြဣၟၤၤၦၩၜၞိီ၇၆ိၛၠၠၢၥၦီဩဤဦဨုၠࠨࡠ")),
        l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡸࠦၼီဧူီ၅ူ၉၈အၝၢၢၤၧၨၜါါဨၠࠧࡡ")),
        l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡹࠧၾဧဤဲူ၇ဲ။ြဣၟၤၤၦၩၜၞိဨုၢࠨࡢ"))
    ), re.MULTILINE | re.DOTALL | re.VERBOSE)
    l11llllll_opy_ = l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡺࠨဧၡၿံႅၩၿၟဩၠࠥࡣ")).format(l1l111111_opy_)
    l11llllll_opy_ = re.compile(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡻࠢၴါႁးႇဳၟࠣࡤ")).format(l11llllll_opy_))
    def l111ll1l_opy_(l1l111l1l_opy_):
        l1lll11l1_opy_ = l1l111l1l_opy_.group(0)
        if l1lll11l1_opy_:
            global l1l1lll1l_opy_
            l11llll1l_opy_[l1l1lll1l_opy_:l1l1lll1l_opy_] = [l1lll11l1_opy_]
            l1l1lll1l_opy_ += 1
        return l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡵࠣါိၤࠧࡥ"))
    l11llll11_opy_ = re.compile(
        l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡶࠤိၮၼၻၭၞၷူၧၩၲၵၶၹၸၭၩၫၜၵီၯၵၺၻၲၶၠၹဲၦႃါူီဪုၦࠨࡦ")), re.MULTILINE)
    l1l11ll11_opy_ = re.compile(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡷࠥၺေဳဧဏဎဦဨဪာဠဢဤဦၤၬာဠဢဤဦဨဪာညဢဤဦဨဪာဠဢာ၅ဩႅြၽါဤဦဨနာဠဢဤဦဨဪာဨ၁ဥႁ္ႇဵဠဢဤတဨဪာဠဢဤဦဨၥၪၜၦၠၝၥဪာဠဌဤဦဨဪာဠဢဤၢၿဴာဠဢဤဦဨဪဖဠဢဤဦဨဪာဠဪ၃၂ဩၩၫဩဢဤဦဒဪာဠဢဤဦဨဪဴဿှဥႁးႇဵဠဢဎဦဨဪာဠဢဤဦူ၉၈အၽဵႃေဪာညဢဤဦဨဪာဠဢၠၨဨဪာဠဢဤဦဨနာဠဢဤိုေၨࠢࡧ")).format(l1l11ll11_opy_, l11llllll_opy_), re.VERBOSE)
    l1l11ll1l_opy_ = re.compile(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡸࠦၼဳၜၤၧၮၺၦၮဧၤࠤࡨ")))
    l11llll1l_opy_ = set(keyword.kwlist + [l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡹࠧဳၟၡၭၴၱၾၫၟဩၦࠥࡩ"))] + l1ll11l1l_opy_)
    l1l111lll_opy_ = [l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡺࠨဧၽဴႃ့ႅွၽဩၧࠥࡪ")).format(l1l1ll11l_opy_, l11ll1l1_opy_)
                            for l11ll1l1_opy_ in l1l11l11l_opy_]
    l1l11l111_opy_ = [
        l1l111lll_opy_ for l1l111lll_opy_ in l1l111lll_opy_ if os.path.exists(l1l111lll_opy_)]
    for l1l111lll_opy_ in l1l11l111_opy_:
        l1l11ll1l_opy_ = open(l1l111lll_opy_)
        content = l1l11ll1l_opy_.read()
        l1l11ll1l_opy_.close()
        content = l1l1l1lll_opy_.sub(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡻࠢဩါၩࠦ࡫")), content)
        content = l1l111l1_opy_.sub(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡵࠣါိၫࠧ࡬")), content)
        l11llll1l_opy_.update(re.findall(l1l11ll11_opy_, content))
    class l1lll11l1_opy_:
        def __init__(self):
            for l1l111l1l_opy_ in l1l1l1ll1_opy_:
                l1l11l11l_opy_ = l1l111l1l_opy_.replace(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡶࠤိံေၮࠢ࡭")), l1l1l1111_opy_)
                try:
                    exec(
                        l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡷࠥုေဳဍဌၭၳၸၹၾၴဢၿံႅဪၭၳဢၧၻၺၼၱၮၶၑၵၬၿၸၥဏဎဦဨဪာဠဢဤဦဨဪာဠဢဤဦဨဪာဠဢဤဦဨဪဳဧဩၫࠥ࡮")).format(l1l111l1l_opy_),
                        globals()
                    )
                    setattr(self, l1l11l11l_opy_, currentModule)
                except Exception as exception:
                    print(exception)
                    setattr(self, l1l11l11l_opy_, None)
                    print(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡸࠦေၣၡၴၲၯၶၱ၆ဠၥၳၻၴၮာၮၱၸဦၱၸၿၰၧၧၺဨၯႄၴၧၶၴၩၶာၭၱၨၻၴၯာၻဲႁိၮࠧ࡯")).format(
                        l1l111l1l_opy_))
    l1l1ll1l_opy_ = l1lll11l1_opy_()
    l1l111l1l_opy_ = set()
    def l1l1ll11l_opy_(l1l1l1111_opy_):
        if l1l1l1111_opy_ in l1l111l1l_opy_:
            return
        else:
            l1l111l1l_opy_.update([l1l1l1111_opy_])
        try:
            l1l111l11_opy_ = list(l1l1l1111_opy_.__dict__)
        except:
            l1l111l11_opy_ = []
        try:
            if l1l1l1lll_opy_:
                l1l11l11l_opy_ = list(l1l1l1111_opy_.func_code.co_varnames)
            else:
                l1l11l11l_opy_ = list(l1l1l1111_opy_.__code__.co_varnames)
        except:
            l1l11l11l_opy_ = []
        l1llll1ll_opy_ = [getattr(l1l1l1111_opy_, l1l11l11l_opy_)
                         for l1l11l11l_opy_ in l1l111l11_opy_]
        l1l1l11ll_opy_ = (l1l1l1111_opy_.join(l1l111l11_opy_)) .split(
            l1l1l1111_opy_)
        l1111111_opy_ = set([entry for entry in (l1l11l11l_opy_ + l1l1l11ll_opy_)
                        if not (entry.startswith(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡹࠧဳၟၡါၮࠦࡰ"))) and entry.endswith(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡺࠨဧၡၣိၰࠧࡱ"))))])
        l11llll1l_opy_.update(l1111111_opy_)
        for attribute in l1llll1ll_opy_:
            try:
                l1l1ll11l_opy_(attribute)
            except:
                pass
    l1l1ll11l_opy_(l1l1ll11l_opy_)
    l1l1ll11l_opy_(l1l1ll1l_opy_)
    l1l1l11ll_opy_ = list(l11llll1l_opy_)
    l1l1l11ll_opy_.sort(key=lambda s: s.lower())
    l1l1l111l_opy_ = []
    l11llllll_opy_ = []
    for l1l1l11ll_opy_ in l1l1ll1ll_opy_:
        if l1l1l11ll_opy_ == l1l1l1ll1_opy_:
            continue
        l11l1111_opy_, l1l11111l_opy_ = l1l1l11ll_opy_.rsplit(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡻࠢဩဳိၱࠧࡲ")), 1)
        l1l1l111l_opy_, l11lllll1_opy_ = (
            l1l11111l_opy_.rsplit(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡵࠣါဴုၳࠨࡳ")), 1) + [l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡶࠤိုၴࠨࡴ"))])[: 2]
        l11lllll1_opy_ = l1l1l11ll_opy_[len(l1l1ll11l_opy_):]
        if l11lllll1_opy_ in l1l1ll11l_opy_ and not l1l1l11ll_opy_ in l1l11l111_opy_:
            l1ll1ll1l_opy_ = random.randrange(64)
            l1lll1ll1_opy_ = codecs.open(l1l1l11ll_opy_, encoding=l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡷࠥုၿႀၦုြိၴࠧࡵ")))
            content = l1lll1ll1_opy_.read()
            l1lll1ll1_opy_.close()
            l1l11ll1l_opy_ = []
            l11llll1l_opy_ = content.split(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡸࠦေၨၮဩၳࠥࡶ")), 2)
            l1l1lll1l_opy_ = 0
            l1l11l1ll_opy_ = True
            if len(l11llll1l_opy_) > 0:
                if l111ll1l_opy_.search(l11llll1l_opy_[0]):
                    l1l1lll1l_opy_ += 1
                    if len(l11llll1l_opy_) > 1 and l1l11l11l_opy_.search(l11llll1l_opy_[1]):
                        l1l1lll1l_opy_ += 1
                        l1l11l1ll_opy_ = False
                elif l1l11l11l_opy_.search(l11llll1l_opy_[0]):
                    l1l1lll1l_opy_ += 1
                    l1l11l1ll_opy_ = False
            if l1111111_opy_ and l1l11l1ll_opy_:
                l11llll1l_opy_[l1l1lll1l_opy_:l1l1lll1l_opy_] = [
                    l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡹࠧဳဣဢၧၵၬၳၺၧြဤၛၜၐ္းဩၴࠥࡷ"))]
                l1l1lll1l_opy_ += 1
            if l1111111_opy_:
                l1l1ll1ll_opy_ = l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡺࠨဧၞၲိၷࠧࡸ")).join(
                    [l1ll1l11l_opy_(l1ll1ll1l_opy_)] + l11llll1l_opy_[l1l1lll1l_opy_:])
            else:
                l1l1ll1ll_opy_ = l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡻࠢဩၠၴုၹࠨࡹ")).join(l11llll1l_opy_[l1l1lll1l_opy_:])
            l1l1ll1ll_opy_ = l1l1l1lll_opy_.sub(
                l1l111111_opy_, l1l1ll1ll_opy_)
            l1lll1ll1_opy_ = []
            l1l1ll1ll_opy_ = l1l111l1_opy_.sub(
                l1l1l11l_opy_, l1l1ll1ll_opy_)
            l1l1ll1ll_opy_ = l11llll11_opy_.sub(l111ll1l_opy_, l1l1ll1ll_opy_)
            l1ll111l1_opy_ = set(re.findall(
                l1l11ll11_opy_, l1l1ll1ll_opy_) + [l1l1l111l_opy_])
            l11llll1l_opy_ = l1ll111l1_opy_.difference(l1l1l111l_opy_).difference(
                l11llll1l_opy_)
            l1ll1111l_opy_ = list(l11llll1l_opy_)
            l111lll1_opy_ = [re.compile(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡵࠣၶိၤၬႇူၿၠၨုၺࠨࡺ")).format(
                l1l11ll11_opy_)) for l1l11ll11_opy_ in l1ll1111l_opy_]
            l1l1l111l_opy_ += l1ll1111l_opy_
            l11llllll_opy_ += l111lll1_opy_
            for l1lll1ll1_opy_, l11ll1l1_opy_ in enumerate(l11llllll_opy_):
                l1l1ll1ll_opy_ = l11ll1l1_opy_.sub(
                    l1ll1111l_opy_(l1lll1ll1_opy_,
                                      l1l1l111l_opy_[l1lll1ll1_opy_]),
                    l1l1ll1ll_opy_
                )
            l1l11llll_opy_ = -1
            l1l1ll1ll_opy_ = l11llllll_opy_.sub(
                l1l1ll1l1_opy_, l1l1ll1ll_opy_)
            l1lll111l_opy_ = -1
            l1l1ll1ll_opy_ = l111l11l_opy_.sub(
                l1l1l1lll_opy_, l1l1ll1ll_opy_)
            content = l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡶࠤိၤၸဳၶࠣࡻ")).join(
                l11llll1l_opy_[:l1l1lll1l_opy_] + [l1l1ll1ll_opy_])
            content = l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡷࠥုၦၺဧၸࠤࡼ")).join([line for line in [line.rstrip()
                                for line in content.split(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡸࠦေၨၮဩၺࠥࡽ")))] if line])
            try:
                l1lll111l_opy_ = l1ll1111l_opy_(
                    l1l1l111l_opy_.index(l1l1l111l_opy_), l1l1l111l_opy_)
            except:
                l1lll111l_opy_ = l1l1l111l_opy_
            l1l11lll1_opy_ = l11lllll1_opy_.split(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡹࠧဳုဩၻࠥࡾ")))
            for index in range(len(l1l11lll1_opy_)):
                try:
                    l1l11lll1_opy_[index] = l1ll1111l_opy_(
                        l1l1l111l_opy_.index(l1l11lll1_opy_[index]), l1l11lll1_opy_[index])
                except:
                    pass
            l11lllll1_opy_ = l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡺࠨဧေါၽࠦࡿ")).join(l1l11lll1_opy_)
            l1l11llll_opy_ = l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡻࠢဩၿံႅႅွၽဩၽࠥࢀ")).format(
                l1l11111l_opy_, l11lllll1_opy_) .rsplit(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡵࠣါဵုႁࠨࢁ")), 1)[0]
            l1l1l11ll_opy_ = l1l1l1ll1_opy_(
                l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡶࠤိႃ်ႉုၽဵႃံႅှၽဩၿࠥࢂ")).format(l1l11llll_opy_, l1lll111l_opy_, l11lllll1_opy_), open=True)
            l1l1l11ll_opy_.write(content)
            l1l1l11ll_opy_.close()
        elif not l11lllll1_opy_ in l1l1l1l1l_opy_:
            l1l11llll_opy_ = l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡷࠥုႅြၽၽဵႃုႃࠨࢃ")).format(
                l1l11111l_opy_, l11lllll1_opy_) .rsplit(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡸࠦေျဧႀࠤࢄ")), 1)[0]
            l1111ll1_opy_ = l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡹࠧဳၻဲႁဵႃျႉဧႁࠤࢅ")).format(l1l11llll_opy_,
                                              l1l11111l_opy_)
            l1l1l1ll1_opy_(l1111ll1_opy_)
            shutil.copyfile(l1l1l11ll_opy_, l1111ll1_opy_)
    print(l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡺࠨဧၑၦၬၽၽၯၡၶၩၪဨႁၻၲၦၷ၀ဨႅြၽဩႃࠥࢆ")).format(len(l1l1l111l_opy_)))
if __name__ == l1l1111ll_opy_ (l1l1ll1_opy_ (u"ࡻࠢဩၣၥၵၫၵၮၡၣိႆࠧࢇ")):
    main()