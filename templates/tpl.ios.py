from string import Template

### Strings

licence = """The MIT License (MIT)

Copyright (c) 2015 Cobaltians

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

### Templates

# FontName.h template
tplfonth = Template("""#import <Foundation/Foundation.h>

#import <Cobalt/CobaltFont.h>

@interface Font${fontkey} : NSObject <CobaltFont>

@end
""")

# FontName.m template
tplfontm = Template("""
#import "Font${fontkey}.h"

@implementation Font${fontkey}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#pragma mark COBALT FONT

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

+ (UIImage *)imageWithIcon:(NSString *)identifier
                     color:(UIColor *)color
                   andSize:(CGSize)size {
    CGFloat scale = [UIScreen mainScreen].scale;
    if ([UIScreen instancesRespondToSelector:@selector(scale)]) {
        UIGraphicsBeginImageContextWithOptions(size, NO, scale);
    }
    else {
        UIGraphicsBeginImageContext(size);
    }
    
    NSString *icon = [Fontt${fontkey} stringForIcon:identifier];
    NSRange iconRange = NSMakeRange(0, icon.length);
    UIColor *backgroundColor = [UIColor clearColor];
    CGRect textRect = CGRectMake(0, 0, size.width, size.height);
    
    UIFont *font = [UIFont fontWithName:@"Fontt${fontkey}"
                                   size:size.height];
    
    NSMutableParagraphStyle *paragraphStyle = [[NSMutableParagraphStyle alloc] init];
    paragraphStyle.alignment = NSTextAlignmentCenter;
    
    NSMutableAttributedString *text = [[NSMutableAttributedString alloc] initWithString:icon];
    [text addAttribute:NSFontAttributeName
                 value:font
                 range:iconRange];
    [text addAttribute:NSForegroundColorAttributeName
                 value:color
                 range:iconRange];
    [text addAttribute:NSBackgroundColorAttributeName
                 value:backgroundColor
                 range:iconRange];
    [text addAttribute:NSParagraphStyleAttributeName
                 value:paragraphStyle
                 range:iconRange];
    [text drawInRect:textRect];
    
    UIImage *image = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    return image;
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#pragma mark FONT

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

+ (NSString *)stringForIcon:(NSString *)identifier {
    return [[Font${fontkey} glyphDictionary] objectForKey:identifier];
}

+ (NSDictionary *)glyphDictionary {
    static NSDictionary *glyphDictionary = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        glyphDictionary = @{${tokenlistkey}};
    });
    
    return glyphDictionary;
}

@end
""")
