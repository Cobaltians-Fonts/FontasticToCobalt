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
    UIColor *backgroundColor = [UIColor clearColor];
    
    CGFloat scale = [UIScreen mainScreen].scale;
    
    if ([UIScreen instancesRespondToSelector:@selector(scale)]) {
        UIGraphicsBeginImageContextWithOptions(size, NO, scale);
    }
    else {
        UIGraphicsBeginImageContext(size);
    }
    
    NSString *text = [Font${fontkey} stringForIcon:identifier];
    CGRect textRect = CGRectZero;
    textRect.size = size;
    
    UIBezierPath *path = [UIBezierPath bezierPathWithRect:textRect];
    [backgroundColor setFill];
    [path fill];
    
    int fontSize = size.width;
    UIFont *font = [UIFont fontWithName:@"Font${fontkey}"
                                   size:fontSize];
    @autoreleasepool {
        UILabel *label = [UILabel new];
        label.font = font;
        label.text = text;
        fontSize = constraintLabelToSize(label, size, 500, 5);
        font = label.font;
    }
    [color setFill];
    [text drawInRect:textRect
      withAttributes:@{NSFontAttributeName: font,
                       NSForegroundColorAttributeName: color,
                       NSBackgroundColorAttributeName: backgroundColor}];
    
    UIImage * image = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    return image;
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#pragma mark HELPERS

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

int constraintLabelToSize(UILabel *label, CGSize size, int maxFontSize, int minFontSize) {
    CGRect rect = CGRectMake(0, 0, size.width, size.height);
    label.frame = rect;
    
    // Try all font sizes from largest to smallest font size
    int fontSize = maxFontSize;
    
    // Fit label width wize
    CGSize constraintSize = CGSizeMake(label.frame.size.width, MAXFLOAT);
    
    do {
        // Set current font size
        label.font = [UIFont fontWithName:label.font.fontName
                                     size:fontSize];
        
        // Find label size for current font size
        CGRect textRect = [[label text] boundingRectWithSize:constraintSize
                                                     options:NSStringDrawingUsesFontLeading
                                                  attributes:@{NSFontAttributeName:label.font}
                                                     context:nil];
        // Done, if created label is within target size
        if( textRect.size.height <= label.frame.size.height )
            break;
        
        // Decrease the font size and try again
        fontSize -= 2;
        
    } while (fontSize > minFontSize);
    
    return fontSize;
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
