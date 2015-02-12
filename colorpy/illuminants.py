'''
illuminants.py - Definitions of some standard illuminants.

Description:

Illuminants are spectrums, normalized so that Y = 1.0.

Spectrums are 2D numpy arrays, with one row for each wavelength,
with the first column holding the wavelength in nm, and the
second column the intensity.

The spectrums have a wavelength increment of 1 nm.

Functions:

init () -
    Initialize CIE Illuminant D65.  This runs on module startup.

get_illuminant_D65 () -
    Get CIE Illuminant D65, as a spectrum, normalized to Y = 1.0.

    CIE standard illuminant D65 represents a phase of natural daylight
    with a correlated color temperature of approximately 6504 K.  (Wyszecki, p. 144)

    In the interest of standardization the CIE recommends that D65 be used
    whenever possible.  Otherwise, D55 or D75 are recommended.  (Wyszecki, p. 145)

    (ColorPy does not currently provide D55 or D75, however.)

get_illuminant_A () -
    Get CIE Illuminant A, as a spectrum, normalized to Y = 1.0.
    This is actually a blackbody illuminant for T = 2856 K.  (Wyszecki, p. 143)

get_blackbody_illuminant (T_K) -
    Get the spectrum of a blackbody at the given temperature, normalized to Y = 1.0.

get_constant_illuminant () -
    Get an illuminant, with spectrum constant over wavelength, normalized to Y = 1.0.

scale_illuminant (illuminant, scaling) -
    Scale the illuminant intensity by the specfied factor.

References:

Wyszecki and Stiles, Color Science: Concepts and Methods, Quantitative Data and Formulae,
    2nd edition, John Wiley, 1982. Wiley Classics Library Edition 2000. ISBN 0-471-39918-3.

CVRL Color and Vision Database - http://cvrl.ioo.ucl.ac.uk/index.htm - (accessed 17 Sep 2008)
    Color and Vision Research Laboratories.
    Provides a set of data sets related to color vision.
    ColorPy uses the tables from this site for the 1931 CIE XYZ matching functions,
    and for Illuminant D65, both at 1 nm wavelength increments.

CIE Standards - http://cvrl.ioo.ucl.ac.uk/cie.htm - (accessed 17 Sep 2008)
    CIE standards as maintained by CVRL.
    The 1931 CIE XYZ and D65 tables that ColorPy uses were obtained from the following files, linked here:
        http://cvrl.ioo.ucl.ac.uk/database/data/cmfs/ciexyz31_1.txt
        http://cvrl.ioo.ucl.ac.uk/database/data/cie/Illuminantd65.txt

CIE International Commission on Illumination - http://www.cie.co.at/ - (accessed 17 Sep 2008)
    Official website of the CIE.
    There are tables of the standard functions (matching functions, illuminants) here:
        http://www.cie.co.at/main/freepubs.html
        http://www.cie.co.at/publ/abst/datatables15_2004/x2.txt
        http://www.cie.co.at/publ/abst/datatables15_2004/y2.txt
        http://www.cie.co.at/publ/abst/datatables15_2004/z2.txt
        http://www.cie.co.at/publ/abst/datatables15_2004/sid65.txt
    ColorPy does not use these specific files.

License:

Copyright (C) 2008 Mark Kness

Author - Mark Kness - mkness@alumni.utexas.net

This file is part of ColorPy.

ColorPy is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

ColorPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with ColorPy.  If not, see <http://www.gnu.org/licenses/>.
'''
import ciexyz
import blackbody
import plots

# table of CIE Illuminant D65 spectrum.
# data from: http://cvrl.ioo.ucl.ac.uk/database/data/cie/Illuminantd65.txt
# massaged into this format.
_Illuminant_D65_table = [
    [ 300, 0.034100 ],
    [ 301, 0.360140 ],
    [ 302, 0.686180 ],
    [ 303, 1.012220 ],
    [ 304, 1.338260 ],
    [ 305, 1.664300 ],
    [ 306, 1.990340 ],
    [ 307, 2.316380 ],
    [ 308, 2.642420 ],
    [ 309, 2.968460 ],
    [ 310, 3.294500 ],
    [ 311, 4.988650 ],
    [ 312, 6.682800 ],
    [ 313, 8.376950 ],
    [ 314, 10.071100 ],
    [ 315, 11.765200 ],
    [ 316, 13.459400 ],
    [ 317, 15.153500 ],
    [ 318, 16.847700 ],
    [ 319, 18.541800 ],
    [ 320, 20.236000 ],
    [ 321, 21.917700 ],
    [ 322, 23.599500 ],
    [ 323, 25.281200 ],
    [ 324, 26.963000 ],
    [ 325, 28.644700 ],
    [ 326, 30.326500 ],
    [ 327, 32.008200 ],
    [ 328, 33.690000 ],
    [ 329, 35.371700 ],
    [ 330, 37.053500 ],
    [ 331, 37.343000 ],
    [ 332, 37.632600 ],
    [ 333, 37.922100 ],
    [ 334, 38.211600 ],
    [ 335, 38.501100 ],
    [ 336, 38.790700 ],
    [ 337, 39.080200 ],
    [ 338, 39.369700 ],
    [ 339, 39.659300 ],
    [ 340, 39.948800 ],
    [ 341, 40.445100 ],
    [ 342, 40.941400 ],
    [ 343, 41.437700 ],
    [ 344, 41.934000 ],
    [ 345, 42.430200 ],
    [ 346, 42.926500 ],
    [ 347, 43.422800 ],
    [ 348, 43.919100 ],
    [ 349, 44.415400 ],
    [ 350, 44.911700 ],
    [ 351, 45.084400 ],
    [ 352, 45.257000 ],
    [ 353, 45.429700 ],
    [ 354, 45.602300 ],
    [ 355, 45.775000 ],
    [ 356, 45.947700 ],
    [ 357, 46.120300 ],
    [ 358, 46.293000 ],
    [ 359, 46.465600 ],
    [ 360, 46.638300 ],
    [ 361, 47.183400 ],
    [ 362, 47.728500 ],
    [ 363, 48.273500 ],
    [ 364, 48.818600 ],
    [ 365, 49.363700 ],
    [ 366, 49.908800 ],
    [ 367, 50.453900 ],
    [ 368, 50.998900 ],
    [ 369, 51.544000 ],
    [ 370, 52.089100 ],
    [ 371, 51.877700 ],
    [ 372, 51.666400 ],
    [ 373, 51.455000 ],
    [ 374, 51.243700 ],
    [ 375, 51.032300 ],
    [ 376, 50.820900 ],
    [ 377, 50.609600 ],
    [ 378, 50.398200 ],
    [ 379, 50.186900 ],
    [ 380, 49.975500 ],
    [ 381, 50.442800 ],
    [ 382, 50.910000 ],
    [ 383, 51.377300 ],
    [ 384, 51.844600 ],
    [ 385, 52.311800 ],
    [ 386, 52.779100 ],
    [ 387, 53.246400 ],
    [ 388, 53.713700 ],
    [ 389, 54.180900 ],
    [ 390, 54.648200 ],
    [ 391, 57.458900 ],
    [ 392, 60.269500 ],
    [ 393, 63.080200 ],
    [ 394, 65.890900 ],
    [ 395, 68.701500 ],
    [ 396, 71.512200 ],
    [ 397, 74.322900 ],
    [ 398, 77.133600 ],
    [ 399, 79.944200 ],
    [ 400, 82.754900 ],
    [ 401, 83.628000 ],
    [ 402, 84.501100 ],
    [ 403, 85.374200 ],
    [ 404, 86.247300 ],
    [ 405, 87.120400 ],
    [ 406, 87.993600 ],
    [ 407, 88.866700 ],
    [ 408, 89.739800 ],
    [ 409, 90.612900 ],
    [ 410, 91.486000 ],
    [ 411, 91.680600 ],
    [ 412, 91.875200 ],
    [ 413, 92.069700 ],
    [ 414, 92.264300 ],
    [ 415, 92.458900 ],
    [ 416, 92.653500 ],
    [ 417, 92.848100 ],
    [ 418, 93.042600 ],
    [ 419, 93.237200 ],
    [ 420, 93.431800 ],
    [ 421, 92.756800 ],
    [ 422, 92.081900 ],
    [ 423, 91.406900 ],
    [ 424, 90.732000 ],
    [ 425, 90.057000 ],
    [ 426, 89.382100 ],
    [ 427, 88.707100 ],
    [ 428, 88.032200 ],
    [ 429, 87.357200 ],
    [ 430, 86.682300 ],
    [ 431, 88.500600 ],
    [ 432, 90.318800 ],
    [ 433, 92.137100 ],
    [ 434, 93.955400 ],
    [ 435, 95.773600 ],
    [ 436, 97.591900 ],
    [ 437, 99.410200 ],
    [ 438, 101.228000 ],
    [ 439, 103.047000 ],
    [ 440, 104.865000 ],
    [ 441, 106.079000 ],
    [ 442, 107.294000 ],
    [ 443, 108.508000 ],
    [ 444, 109.722000 ],
    [ 445, 110.936000 ],
    [ 446, 112.151000 ],
    [ 447, 113.365000 ],
    [ 448, 114.579000 ],
    [ 449, 115.794000 ],
    [ 450, 117.008000 ],
    [ 451, 117.088000 ],
    [ 452, 117.169000 ],
    [ 453, 117.249000 ],
    [ 454, 117.330000 ],
    [ 455, 117.410000 ],
    [ 456, 117.490000 ],
    [ 457, 117.571000 ],
    [ 458, 117.651000 ],
    [ 459, 117.732000 ],
    [ 460, 117.812000 ],
    [ 461, 117.517000 ],
    [ 462, 117.222000 ],
    [ 463, 116.927000 ],
    [ 464, 116.632000 ],
    [ 465, 116.336000 ],
    [ 466, 116.041000 ],
    [ 467, 115.746000 ],
    [ 468, 115.451000 ],
    [ 469, 115.156000 ],
    [ 470, 114.861000 ],
    [ 471, 114.967000 ],
    [ 472, 115.073000 ],
    [ 473, 115.180000 ],
    [ 474, 115.286000 ],
    [ 475, 115.392000 ],
    [ 476, 115.498000 ],
    [ 477, 115.604000 ],
    [ 478, 115.711000 ],
    [ 479, 115.817000 ],
    [ 480, 115.923000 ],
    [ 481, 115.212000 ],
    [ 482, 114.501000 ],
    [ 483, 113.789000 ],
    [ 484, 113.078000 ],
    [ 485, 112.367000 ],
    [ 486, 111.656000 ],
    [ 487, 110.945000 ],
    [ 488, 110.233000 ],
    [ 489, 109.522000 ],
    [ 490, 108.811000 ],
    [ 491, 108.865000 ],
    [ 492, 108.920000 ],
    [ 493, 108.974000 ],
    [ 494, 109.028000 ],
    [ 495, 109.082000 ],
    [ 496, 109.137000 ],
    [ 497, 109.191000 ],
    [ 498, 109.245000 ],
    [ 499, 109.300000 ],
    [ 500, 109.354000 ],
    [ 501, 109.199000 ],
    [ 502, 109.044000 ],
    [ 503, 108.888000 ],
    [ 504, 108.733000 ],
    [ 505, 108.578000 ],
    [ 506, 108.423000 ],
    [ 507, 108.268000 ],
    [ 508, 108.112000 ],
    [ 509, 107.957000 ],
    [ 510, 107.802000 ],
    [ 511, 107.501000 ],
    [ 512, 107.200000 ],
    [ 513, 106.898000 ],
    [ 514, 106.597000 ],
    [ 515, 106.296000 ],
    [ 516, 105.995000 ],
    [ 517, 105.694000 ],
    [ 518, 105.392000 ],
    [ 519, 105.091000 ],
    [ 520, 104.790000 ],
    [ 521, 105.080000 ],
    [ 522, 105.370000 ],
    [ 523, 105.660000 ],
    [ 524, 105.950000 ],
    [ 525, 106.239000 ],
    [ 526, 106.529000 ],
    [ 527, 106.819000 ],
    [ 528, 107.109000 ],
    [ 529, 107.399000 ],
    [ 530, 107.689000 ],
    [ 531, 107.361000 ],
    [ 532, 107.032000 ],
    [ 533, 106.704000 ],
    [ 534, 106.375000 ],
    [ 535, 106.047000 ],
    [ 536, 105.719000 ],
    [ 537, 105.390000 ],
    [ 538, 105.062000 ],
    [ 539, 104.733000 ],
    [ 540, 104.405000 ],
    [ 541, 104.369000 ],
    [ 542, 104.333000 ],
    [ 543, 104.297000 ],
    [ 544, 104.261000 ],
    [ 545, 104.225000 ],
    [ 546, 104.190000 ],
    [ 547, 104.154000 ],
    [ 548, 104.118000 ],
    [ 549, 104.082000 ],
    [ 550, 104.046000 ],
    [ 551, 103.641000 ],
    [ 552, 103.237000 ],
    [ 553, 102.832000 ],
    [ 554, 102.428000 ],
    [ 555, 102.023000 ],
    [ 556, 101.618000 ],
    [ 557, 101.214000 ],
    [ 558, 100.809000 ],
    [ 559, 100.405000 ],
    [ 560, 100.000000 ],
    [ 561, 99.633400 ],
    [ 562, 99.266800 ],
    [ 563, 98.900300 ],
    [ 564, 98.533700 ],
    [ 565, 98.167100 ],
    [ 566, 97.800500 ],
    [ 567, 97.433900 ],
    [ 568, 97.067400 ],
    [ 569, 96.700800 ],
    [ 570, 96.334200 ],
    [ 571, 96.279600 ],
    [ 572, 96.225000 ],
    [ 573, 96.170300 ],
    [ 574, 96.115700 ],
    [ 575, 96.061100 ],
    [ 576, 96.006500 ],
    [ 577, 95.951900 ],
    [ 578, 95.897200 ],
    [ 579, 95.842600 ],
    [ 580, 95.788000 ],
    [ 581, 95.077800 ],
    [ 582, 94.367500 ],
    [ 583, 93.657300 ],
    [ 584, 92.947000 ],
    [ 585, 92.236800 ],
    [ 586, 91.526600 ],
    [ 587, 90.816300 ],
    [ 588, 90.106100 ],
    [ 589, 89.395800 ],
    [ 590, 88.685600 ],
    [ 591, 88.817700 ],
    [ 592, 88.949700 ],
    [ 593, 89.081800 ],
    [ 594, 89.213800 ],
    [ 595, 89.345900 ],
    [ 596, 89.478000 ],
    [ 597, 89.610000 ],
    [ 598, 89.742100 ],
    [ 599, 89.874100 ],
    [ 600, 90.006200 ],
    [ 601, 89.965500 ],
    [ 602, 89.924800 ],
    [ 603, 89.884100 ],
    [ 604, 89.843400 ],
    [ 605, 89.802600 ],
    [ 606, 89.761900 ],
    [ 607, 89.721200 ],
    [ 608, 89.680500 ],
    [ 609, 89.639800 ],
    [ 610, 89.599100 ],
    [ 611, 89.409100 ],
    [ 612, 89.219000 ],
    [ 613, 89.029000 ],
    [ 614, 88.838900 ],
    [ 615, 88.648900 ],
    [ 616, 88.458900 ],
    [ 617, 88.268800 ],
    [ 618, 88.078800 ],
    [ 619, 87.888700 ],
    [ 620, 87.698700 ],
    [ 621, 87.257700 ],
    [ 622, 86.816700 ],
    [ 623, 86.375700 ],
    [ 624, 85.934700 ],
    [ 625, 85.493600 ],
    [ 626, 85.052600 ],
    [ 627, 84.611600 ],
    [ 628, 84.170600 ],
    [ 629, 83.729600 ],
    [ 630, 83.288600 ],
    [ 631, 83.329700 ],
    [ 632, 83.370700 ],
    [ 633, 83.411800 ],
    [ 634, 83.452800 ],
    [ 635, 83.493900 ],
    [ 636, 83.535000 ],
    [ 637, 83.576000 ],
    [ 638, 83.617100 ],
    [ 639, 83.658100 ],
    [ 640, 83.699200 ],
    [ 641, 83.332000 ],
    [ 642, 82.964700 ],
    [ 643, 82.597500 ],
    [ 644, 82.230200 ],
    [ 645, 81.863000 ],
    [ 646, 81.495800 ],
    [ 647, 81.128500 ],
    [ 648, 80.761300 ],
    [ 649, 80.394000 ],
    [ 650, 80.026800 ],
    [ 651, 80.045600 ],
    [ 652, 80.064400 ],
    [ 653, 80.083100 ],
    [ 654, 80.101900 ],
    [ 655, 80.120700 ],
    [ 656, 80.139500 ],
    [ 657, 80.158300 ],
    [ 658, 80.177000 ],
    [ 659, 80.195800 ],
    [ 660, 80.214600 ],
    [ 661, 80.420900 ],
    [ 662, 80.627200 ],
    [ 663, 80.833600 ],
    [ 664, 81.039900 ],
    [ 665, 81.246200 ],
    [ 666, 81.452500 ],
    [ 667, 81.658800 ],
    [ 668, 81.865200 ],
    [ 669, 82.071500 ],
    [ 670, 82.277800 ],
    [ 671, 81.878400 ],
    [ 672, 81.479100 ],
    [ 673, 81.079700 ],
    [ 674, 80.680400 ],
    [ 675, 80.281000 ],
    [ 676, 79.881600 ],
    [ 677, 79.482300 ],
    [ 678, 79.082900 ],
    [ 679, 78.683600 ],
    [ 680, 78.284200 ],
    [ 681, 77.427900 ],
    [ 682, 76.571600 ],
    [ 683, 75.715300 ],
    [ 684, 74.859000 ],
    [ 685, 74.002700 ],
    [ 686, 73.146500 ],
    [ 687, 72.290200 ],
    [ 688, 71.433900 ],
    [ 689, 70.577600 ],
    [ 690, 69.721300 ],
    [ 691, 69.910100 ],
    [ 692, 70.098900 ],
    [ 693, 70.287600 ],
    [ 694, 70.476400 ],
    [ 695, 70.665200 ],
    [ 696, 70.854000 ],
    [ 697, 71.042800 ],
    [ 698, 71.231500 ],
    [ 699, 71.420300 ],
    [ 700, 71.609100 ],
    [ 701, 71.883100 ],
    [ 702, 72.157100 ],
    [ 703, 72.431100 ],
    [ 704, 72.705100 ],
    [ 705, 72.979000 ],
    [ 706, 73.253000 ],
    [ 707, 73.527000 ],
    [ 708, 73.801000 ],
    [ 709, 74.075000 ],
    [ 710, 74.349000 ],
    [ 711, 73.074500 ],
    [ 712, 71.800000 ],
    [ 713, 70.525500 ],
    [ 714, 69.251000 ],
    [ 715, 67.976500 ],
    [ 716, 66.702000 ],
    [ 717, 65.427500 ],
    [ 718, 64.153000 ],
    [ 719, 62.878500 ],
    [ 720, 61.604000 ],
    [ 721, 62.432200 ],
    [ 722, 63.260300 ],
    [ 723, 64.088500 ],
    [ 724, 64.916600 ],
    [ 725, 65.744800 ],
    [ 726, 66.573000 ],
    [ 727, 67.401100 ],
    [ 728, 68.229300 ],
    [ 729, 69.057400 ],
    [ 730, 69.885600 ],
    [ 731, 70.405700 ],
    [ 732, 70.925900 ],
    [ 733, 71.446000 ],
    [ 734, 71.966200 ],
    [ 735, 72.486300 ],
    [ 736, 73.006400 ],
    [ 737, 73.526600 ],
    [ 738, 74.046700 ],
    [ 739, 74.566900 ],
    [ 740, 75.087000 ],
    [ 741, 73.937600 ],
    [ 742, 72.788100 ],
    [ 743, 71.638700 ],
    [ 744, 70.489300 ],
    [ 745, 69.339800 ],
    [ 746, 68.190400 ],
    [ 747, 67.041000 ],
    [ 748, 65.891600 ],
    [ 749, 64.742100 ],
    [ 750, 63.592700 ],
    [ 751, 61.875200 ],
    [ 752, 60.157800 ],
    [ 753, 58.440300 ],
    [ 754, 56.722900 ],
    [ 755, 55.005400 ],
    [ 756, 53.288000 ],
    [ 757, 51.570500 ],
    [ 758, 49.853100 ],
    [ 759, 48.135600 ],
    [ 760, 46.418200 ],
    [ 761, 48.456900 ],
    [ 762, 50.495600 ],
    [ 763, 52.534400 ],
    [ 764, 54.573100 ],
    [ 765, 56.611800 ],
    [ 766, 58.650500 ],
    [ 767, 60.689200 ],
    [ 768, 62.728000 ],
    [ 769, 64.766700 ],
    [ 770, 66.805400 ],
    [ 771, 66.463100 ],
    [ 772, 66.120900 ],
    [ 773, 65.778600 ],
    [ 774, 65.436400 ],
    [ 775, 65.094100 ],
    [ 776, 64.751800 ],
    [ 777, 64.409600 ],
    [ 778, 64.067300 ],
    [ 779, 63.725100 ],
    [ 780, 63.382800 ],
    [ 781, 63.474900 ],
    [ 782, 63.567000 ],
    [ 783, 63.659200 ],
    [ 784, 63.751300 ],
    [ 785, 63.843400 ],
    [ 786, 63.935500 ],
    [ 787, 64.027600 ],
    [ 788, 64.119800 ],
    [ 789, 64.211900 ],
    [ 790, 64.304000 ],
    [ 791, 63.818800 ],
    [ 792, 63.333600 ],
    [ 793, 62.848400 ],
    [ 794, 62.363200 ],
    [ 795, 61.877900 ],
    [ 796, 61.392700 ],
    [ 797, 60.907500 ],
    [ 798, 60.422300 ],
    [ 799, 59.937100 ],
    [ 800, 59.451900 ],
    [ 801, 58.702600 ],
    [ 802, 57.953300 ],
    [ 803, 57.204000 ],
    [ 804, 56.454700 ],
    [ 805, 55.705400 ],
    [ 806, 54.956200 ],
    [ 807, 54.206900 ],
    [ 808, 53.457600 ],
    [ 809, 52.708300 ],
    [ 810, 51.959000 ],
    [ 811, 52.507200 ],
    [ 812, 53.055300 ],
    [ 813, 53.603500 ],
    [ 814, 54.151600 ],
    [ 815, 54.699800 ],
    [ 816, 55.248000 ],
    [ 817, 55.796100 ],
    [ 818, 56.344300 ],
    [ 819, 56.892400 ],
    [ 820, 57.440600 ],
    [ 821, 57.727800 ],
    [ 822, 58.015000 ],
    [ 823, 58.302200 ],
    [ 824, 58.589400 ],
    [ 825, 58.876500 ],
    [ 826, 59.163700 ],
    [ 827, 59.450900 ],
    [ 828, 59.738100 ],
    [ 829, 60.025300 ],
    [ 830, 60.312500 ]
]

_Illuminant_D65 = None

def init ():
    '''Initialize CIE Illuminant D65.  This runs on module startup.'''
    first_wl = _Illuminant_D65_table [0][0]
    # for now, only consider the part in the normal visible range (360-830 nm)
    first_index = ciexyz.start_wl_nm - first_wl
    table_first = _Illuminant_D65_table [first_index][0]
    assert (table_first == 360), 'Mismatch finding 360 nm entry in D65 table'
    global _Illuminant_D65
    _Illuminant_D65 = ciexyz.empty_spectrum()
    (num_wl, num_cols) = _Illuminant_D65.shape
    for i in range (0, num_wl):
        _Illuminant_D65 [i][1] = _Illuminant_D65_table [first_index + i][1]
    # normalization - illuminant is scaled so that Y = 1.0
    xyz = ciexyz.xyz_from_spectrum (_Illuminant_D65)
    scaling = 1.0 / xyz [1]
    _Illuminant_D65 [:,1] *= scaling

#
# Get any of the available illuminants - D65, A, any blackbody, or a constant spectrum.
# ColorPy does not currently provide D55 or D75.
#

def get_illuminant_D65 ():
    '''Get CIE Illuminant D65, as a spectrum, normalized to Y = 1.0.

    CIE standard illuminant D65 represents a phase of natural daylight
    with a correlated color temperature of approximately 6504 K.  (Wyszecki, p. 144)

    In the interest of standardization the CIE recommends that D65 be used
    whenever possible.  Otherwise, D55 or D75 are recommended.  (Wyszecki, p. 145)

    (ColorPy does not currently provide D55 or D75, however.)'''
    illuminant = _Illuminant_D65.copy()
    return illuminant

def get_illuminant_A ():
    '''Get CIE Illuminant A, as a spectrum, normalized to Y = 1.0.
    This is actually a blackbody illuminant for T = 2856 K.  (Wyszecki, p. 143)'''
    illuminant = get_blackbody_illuminant (2856.0)
    return illuminant

def get_blackbody_illuminant (T_K):
    '''Get the spectrum of a blackbody at the given temperature, normalized to Y = 1.0.'''
    illuminant = blackbody.blackbody_spectrum (T_K)
    xyz = ciexyz.xyz_from_spectrum (illuminant)
    if xyz [1] != 0.0:
        scaling = 1.0 / xyz [1]
        illuminant [:,1] *= scaling
    return illuminant

def get_constant_illuminant ():
    '''Get an illuminant, with spectrum constant over wavelength, normalized to Y = 1.0.'''
    illuminant = ciexyz.empty_spectrum()
    (num_wl, num_cols) = illuminant.shape
    for i in range (0, num_wl):
        illuminant [i][1] = 1.0
    xyz = ciexyz.xyz_from_spectrum (illuminant)
    if xyz [1] != 0.0:
        scaling = 1.0 / xyz [1]
        illuminant [:,1] *= scaling
    return illuminant

# Scale an illuminant by an arbitrary factor

def scale_illuminant (illuminant, scaling):
    '''Scale the illuminant intensity by the specfied factor.'''
    illuminant [:,1] *= scaling
    return illuminant

# Initialize at module startup
init()

# Figures - Plot some of the illuminants

def figures ():
    '''Plot spectra for several illuminants.'''
    # D65
    plots.spectrum_plot (
        get_illuminant_D65(), 'CIE Illuminant D65', 'Illuminant-D65')
    # A
    plots.spectrum_plot (
        get_illuminant_A(), 'CIE Illuminant A', 'Illuminant-A')
    # Constant
    plots.spectrum_plot (
        get_constant_illuminant(), 'Constant Illuminant', 'Illuminant-Const')
    # Blackbody (5778)
    plots.spectrum_plot (
        get_blackbody_illuminant (5778.0), '5778 K Illuminant', 'Illuminant-5778')
